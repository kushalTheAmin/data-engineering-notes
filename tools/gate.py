#!/usr/bin/env python3
"""Mechanical QA gate for this notes repo.

Usage: python3 tools/gate.py
Prints one FAIL line per problem, then PASS or FAIL. Exit code 0 only on PASS.

Every note gets the structure checks: header, footer chain, links, tables,
and every sql and python block is rerun and its result compared.
Notes changed since origin/main (or the newest note, if there is no remote)
also get the full checks: word count, voice, notation, mermaid rendering.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_DIR = os.path.join(ROOT, "notes")
SHOP_SQL = os.path.join(ROOT, "data", "shop.sql")

NOTE_FILE = re.compile(r"^(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
DASH_CHARS = "\u2012\u2013\u2014\u2015"
GREEK = re.compile("[\u0370-\u03ff\u1f00-\u1fff]")
MATH = re.compile("[\u2211\u220f\u222b\u221a\u221e\u2248\u2202\u2206\u2207]")
ATTRIBUTION = re.compile(r"claude|anthropic|co-authored-by|\U0001F916", re.I)
COMMIT_ATTRIBUTION = re.compile(r"claude|anthropic|co-authored-by|generated with|\U0001F916", re.I)
COMMIT_SUBJECT = re.compile(r"^(note \d{3}: \S.*|curriculum: (split|add) \S.*|log: \S.*|audit \d{3}: \S.*)$")
ALLOWED_CHANGES = re.compile(r"^(notes/\d{3}-[a-z0-9-]+\.md|checks/\d{3}\.py|curriculum\.md|README\.md|glossary\.md|data/shop\.sql)$")

fails = []
infos = []


def fail(where, msg):
    fails.append(f"FAIL {where}: {msg}")


def git(*args):
    try:
        r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout
    except FileNotFoundError:
        return 1, ""


# ---------- parsing ----------

def segments(lines, where):
    """Split note lines into ('prose', index, line) and ('code', lang, body_lines) items."""
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip().lower()
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                fail(where, "a code block is never closed")
            out.append(("code", lang, body))
            i += 1
            continue
        out.append(("prose", i, line))
        i += 1
    return out


def footer_start(lines):
    """Index of the '---' line that opens the footer, or None."""
    nonblank = [i for i, l in enumerate(lines) if l.strip()]
    if len(nonblank) < 2:
        return None
    last, before = nonblank[-1], nonblank[-2]
    if lines[last].startswith("prev:") and lines[before].strip() == "---":
        return before
    return None


QUIZ_HEADING = "### check yourself"
HTML_LINE = re.compile(r"^\s*(<details>\s*<summary>answer</summary>|</details>)\s*$")


def quiz_start(lines):
    """Index of the check yourself heading, or None."""
    for i, l in enumerate(lines):
        if l.strip() == QUIZ_HEADING:
            return i
    return None


def prose_lines(lines, where, part="body"):
    """Prose only: no header, footer, code, tables, blank or answer-tag lines.
    part='body' is everything before the check yourself heading, part='quiz' is the section itself."""
    end = footer_start(lines)
    end = len(lines) if end is None else end
    q = quiz_start(lines)
    lo, hi = (3, q if q is not None else end) if part == "body" else ((q + 1, end) if q is not None else (0, 0))
    result = []
    for seg in segments(lines[:end], where):
        if seg[0] != "prose":
            continue
        idx, line = seg[1], seg[2]
        if not lo <= idx < hi or not line.strip() or line.lstrip().startswith("|") or HTML_LINE.match(line):
            continue
        result.append(line)
    return result


def check_quiz(where, lines, required, practice=False):
    """The check yourself section: 2 or 3 numbered questions, each with a hidden answer."""
    q = quiz_start(lines)
    if q is None:
        if required:
            fail(where, "this concept is starred or a capstone, so the note needs a '### check yourself' section")
        return
    end = footer_start(lines)
    end = len(lines) if end is None else end
    if q >= end:
        fail(where, "'### check yourself' must sit above the footer")
        return
    section = lines[q + 1:end]
    in_code = False
    questions, opens, closes = [], [], []
    for k, l in enumerate(section):
        if l.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(\d+)\. \S", l)
        if m:
            questions.append((k, int(m.group(1))))
        if re.match(r"^\s*<details>\s*<summary>answer</summary>\s*$", l):
            opens.append(k)
            if k + 1 >= len(section) or section[k + 1].strip():
                fail(where, "leave a blank line after <details><summary>answer</summary> or github wont render the answer")
        elif "<details" in l or "<summary" in l:
            fail(where, "answers open with exactly '<details><summary>answer</summary>' on its own line")
        if re.match(r"^\s*</details>\s*$", l):
            closes.append(k)
            if k == 0 or section[k - 1].strip():
                fail(where, "leave a blank line before </details>")
    low, high = (3, 10) if practice else (2, 3)
    if not low <= len(questions) <= high:
        fail(where, f"check yourself needs {low} to {high} numbered questions, found {len(questions)}")
    if [n for _, n in questions] != list(range(1, len(questions) + 1)):
        fail(where, "questions must be numbered 1. 2. 3. in order")
    if not (len(opens) == len(closes) == len(questions)):
        fail(where, "every question needs exactly one hidden answer: <details><summary>answer</summary> ... </details>")
    else:
        bounds = [k for k, _ in questions] + [len(section)]
        for i in range(len(questions)):
            if not (bounds[i] < opens[i] < closes[i] < bounds[i + 1]):
                fail(where, f"question {i + 1}: its hidden answer must come after it and before the next question")
    words = word_count([re.sub(r"<[^>]+>", " ", l) for l in prose_lines(lines, where, "quiz")])
    cap = 600 if practice else 200
    if words > cap:
        fail(where, f"check yourself is {words} words, keep questions plus answers under {cap}")


def strip_markup(text):
    text = LINK.sub(r"\1", text)
    return text.replace("**", " ").replace("__", " ")


def word_count(prose):
    words = strip_markup(" ".join(prose)).split()
    return sum(1 for w in words if re.search(r"[A-Za-z0-9]", w))


def note_number(name):
    m = NOTE_FILE.match(name)
    return int(m.group(1)) if m else None


# ---------- code block checks ----------

def fmt_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return repr(v)
    return str(v)


def parse_result_block(body):
    rows = [l for l in body if l.strip()]
    return [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]


def check_sql(where, con, sql, expected):
    on_purpose = "fails on purpose" in sql.lower()
    try:
        stmts = con.extract_statements(sql)
        cur = None
        for s in stmts:
            cur = con.execute(s)
    except Exception as e:
        if not on_purpose:
            fail(where, f"sql block errors: {str(e).splitlines()[0]}")
        return
    if on_purpose:
        fail(where, "a sql block marked 'fails on purpose' ran without an error")
        return
    if expected is None:
        return
    if cur is None or cur.description is None:
        fail(where, "a result block follows sql that returns no rows")
        return
    header = [d[0] for d in cur.description]
    got = [header] + [[fmt_value(v) for v in row] for row in cur.fetchall()]
    want = parse_result_block(expected)
    if not want or want[0] != header:
        fail(where, f"result header should be {' | '.join(header)}")
        return
    if "order by" not in sql.lower():
        got = [got[0]] + sorted(got[1:])
        want = [want[0]] + sorted(want[1:])
    if got != want:
        for g, w in zip(got, want):
            if g != w:
                fail(where, f"result row is {' | '.join(w)} but the query gives {' | '.join(g)}")
                return
        fail(where, f"result block has {len(want) - 1} rows, the query gives {len(got) - 1}")


def check_python(where, code, expected):
    src = "\n".join(code)
    try:
        compile(src, "<note>", "exec")
    except SyntaxError as e:
        fail(where, f"python block does not compile: {e.msg} (line {e.lineno})")
        return
    if expected is None:
        return
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "block.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(src)
        try:
            r = subprocess.run([sys.executable, "-I", path], cwd=d, capture_output=True, text=True, timeout=20)
        except subprocess.TimeoutExpired:
            fail(where, "python block ran longer than 20 seconds")
            return
    if r.returncode != 0:
        fail(where, f"python block raised: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'error'}")
        return
    got = [l.rstrip() for l in r.stdout.rstrip("\n").split("\n")]
    want = [l.rstrip() for l in "\n".join(expected).rstrip("\n").split("\n")]
    if got != want:
        fail(where, f"output block does not match what the python prints (it prints: {' / '.join(got[:4])})")


MERMAID_STATE = {"ok": None}


def check_mermaid(where, body):
    with tempfile.TemporaryDirectory() as d:
        src, out = os.path.join(d, "in.mmd"), os.path.join(d, "out.svg")
        with open(src, "w", encoding="utf-8") as f:
            f.write("\n".join(body))
        try:
            r = subprocess.run(
                ["npx", "-y", "@mermaid-js/mermaid-cli", "-q", "-i", src, "-o", out],
                capture_output=True, text=True, timeout=240)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            fail(where, "mermaid renderer unavailable, so no mermaid today: pick another visual type")
            return
        if r.returncode == 0 and os.path.exists(out):
            return
        msg = (r.stderr or r.stdout).strip()
        if "Parse error" in msg or "Syntax error" in msg or "Lexical error" in msg:
            first = [l for l in msg.splitlines() if l.strip()][:2]
            fail(where, "mermaid does not render: " + " ".join(first))
        else:
            fail(where, "mermaid renderer unavailable, so no mermaid today: pick another visual type")


# ---------- verification files ----------

URL = re.compile(r"^https?://\S+\.\S+$")


def check_verification(where, n):
    """checks/NNN.py must exist, assert the notes facts, cite sources as urls, and pass."""
    path = os.path.join(ROOT, "checks", f"{n:03d}.py")
    if not os.path.exists(path):
        fail(where, f"missing checks/{n:03d}.py: every number and fact in the note needs its verification file")
        return
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if "assert" not in src:
        fail(f"checks/{n:03d}.py", "has no assert: every number and computable fact in the note gets one")
    for line in src.split("\n"):
        m = re.match(r"^\s*#\s*source:\s*(.*)$", line)
        if m and not URL.match(m.group(1).strip()):
            fail(f"checks/{n:03d}.py", f"source must be a url that was opened: {line.strip()[:60]}")
    try:
        r = subprocess.run([sys.executable, "-I", path], cwd=ROOT, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        fail(f"checks/{n:03d}.py", "ran longer than 120 seconds")
        return
    if r.returncode != 0:
        last = (r.stderr.strip().splitlines() or ["error"])[-1]
        fail(f"checks/{n:03d}.py", f"a check failed: {last[:120]}")


# ---------- per note ----------

def check_note(path, all_names, full, quiz_required, practice=False):
    name = os.path.basename(path)
    where = f"notes/{name}"
    n = note_number(name)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    newest = max(note_number(x) for x in all_names)
    by_num = {note_number(x): x for x in all_names}

    # header
    m = re.match(r"^# (\d{3}): \S", lines[0] if lines else "")
    if not m or int(m.group(1)) != n:
        fail(where, f"line 1 must be '# {n:03d}: <title>'")
    if len(lines) < 3:
        fail(where, "header needs three lines: title, builds on, section")
        return
    if n == 1:
        if lines[1] != "builds on: nothing, this is the start":
            fail(where, "note 001 line 2 must be 'builds on: nothing, this is the start'")
    else:
        targets = LINK.findall(lines[1])
        if not lines[1].startswith("builds on: ") or not targets:
            fail(where, "line 2 must be 'builds on: ' followed by links to earlier notes")
        for _, t in targets:
            tn = note_number(os.path.basename(t))
            if tn is None or tn >= n:
                fail(where, f"builds on links to {t}, which is not an earlier note")
    capstone = lines[2].endswith(", wrap up, ~3 min read")
    if not re.match(r"^section: \S.*, (part \d+, ~2 min read|wrap up, ~3 min read)$", lines[2]):
        fail(where, "line 3 must look like 'section: <arc name>, part <n>, ~2 min read' (capstones: ', wrap up, ~3 min read')")

    # footer chain
    fs = footer_start(lines)
    if fs is None:
        fail(where, "footer missing: last two lines must be '---' then 'prev: ... | next: ...'")
    else:
        foot = [l for l in lines[fs + 1:] if l.strip()][0]
        parts = foot.split(" | ")
        if len(parts) != 2 or not parts[1].startswith("next: "):
            fail(where, "footer must be 'prev: ... | next: ...'")
        else:
            prev, nxt = parts
            if n == 1:
                if prev != "prev: nothing, this is the start":
                    fail(where, "note 001 footer must start 'prev: nothing, this is the start'")
            else:
                want = by_num.get(n - 1)
                got = LINK.findall(prev)
                if not got or os.path.basename(got[0][1]) != want or got[0][1] != f"./{want}":
                    fail(where, f"footer prev must link to ./{want}")
            if n == newest:
                if nxt != "next: not written yet":
                    fail(where, "newest note footer must end 'next: not written yet'")
            else:
                want = by_num.get(n + 1)
                got = LINK.findall(nxt)
                if not got or got[0][1] != f"./{want}":
                    fail(where, f"footer next must link to ./{want} (update it when the next note ships)")

    segs = segments(lines, where)

    # links outside code
    for seg in segs:
        if seg[0] != "prose":
            continue
        for _, target in LINK.findall(seg[2]):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target.split("#")[0]))
            if not os.path.exists(resolved):
                fail(where, f"link target does not exist: {target}")

    # tables: same cell count on every row, separator on row 2
    table = []
    for seg in segs + [("prose", -1, "")]:
        is_row = seg[0] == "prose" and seg[2].lstrip().startswith("|")
        if is_row:
            table.append(seg[2])
            continue
        if table:
            counts = {len(r.strip().strip("|").split("|")) for r in table}
            if len(counts) != 1:
                fail(where, f"table starting '{table[0][:40]}' has rows with different cell counts")
            if len(table) < 2 or not re.match(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$", table[1].strip()):
                fail(where, f"table starting '{table[0][:40]}' needs a |---| separator as its second row")
            table = []

    # code blocks: sql and python are rerun, result and output must follow them
    code = [s for s in segs if s[0] == "code"]
    con = None
    for k, seg in enumerate(segs):
        if seg[0] != "code":
            continue
        lang, body = seg[1], seg[2]
        nxt = None
        for later in segs[k + 1:]:
            if later[0] == "prose" and (not later[2].strip() or HTML_LINE.match(later[2])):
                continue
            nxt = later if later[0] == "code" else None
            break
        if lang == "sql":
            if con is None:
                import duckdb
                con = duckdb.connect(":memory:")
                with open(SHOP_SQL, encoding="utf-8") as f:
                    con.execute(f.read())
            expected = nxt[2] if nxt and nxt[1] == "result" else None
            check_sql(where, con, "\n".join(body), expected)
        elif lang == "python":
            expected = nxt[2] if nxt and nxt[1] == "output" else None
            check_python(where, body, expected)
        elif lang == "json":
            try:
                json.loads("\n".join(body))
            except ValueError as e:
                fail(where, f"json block does not parse: {e}")
        elif lang in ("result", "output"):
            prev_code = None
            for earlier in reversed(segs[:k]):
                if earlier[0] == "prose" and (not earlier[2].strip() or HTML_LINE.match(earlier[2])):
                    continue
                prev_code = earlier
                break
            need = "sql" if lang == "result" else "python"
            if not prev_code or prev_code[0] != "code" or prev_code[1] != need:
                fail(where, f"a ```{lang} block must sit right under a ```{need} block")
        elif lang == "mermaid" and full:
            check_mermaid(where, body)
        elif lang == "":
            fail(where, "every code block needs a language tag (sql, result, python, output, mermaid, text, csv, json, bash)")

    check_quiz(where, lines, quiz_required, practice)
    check_verification(where, n)

    if not full:
        return

    # whole-file character scans
    for ch in DASH_CHARS:
        if ch in text:
            fail(where, f"contains a long dash character (U+{ord(ch):04X})")
    if GREEK.search(text) or MATH.search(text):
        fail(where, "contains a greek letter or math symbol")
    if ATTRIBUTION.search(text):
        fail(where, "contains an attribution string")

    # prose checks
    prose = prose_lines(lines, where)
    words = word_count(prose)
    low, high = (120, 350) if capstone else (120, 250)
    if not low <= words <= high:
        fail(where, f"prose is {words} words, must be {low} to {high}")
    def clean(ls):
        return [re.sub(r"`[^`]*`", " ", LINK.sub(r"\1", l)) for l in ls]
    plain = clean(prose)
    quiz = clean(prose_lines(lines, where, "quiz"))
    joined = " ".join(plain)
    everything = " ".join(plain + quiz)
    if re.search("[A-Za-z][\u2019'][A-Za-z]", everything):
        fail(where, "prose has an apostrophe: write dont, its, ashas, never don't")
    if re.search(r"(?<![\w/])I(?![\w/])", everything):
        fail(where, "prose has a capital I: lowercase i always")
    if not re.search(r"\b(i|im|ive|ill)\b", joined):
        fail(where, "no first person: a real 'i' has to appear")
    if not re.search(r"\b(you|your|youre|youll|youd)\b", joined, re.I):
        fail(where, "never talks to the reader: 'you' has to appear")
    for l in plain + quiz:
        body = re.sub(r"^\s*([-*]|\d+\.)\s+", "", l)
        if re.search(r"\s-{1,2}\s", body):
            fail(where, f"hyphen used as a dash in: '{body.strip()[:50]}'")


# ---------- repo level ----------

def scan_file(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        fail(rel, "missing")
        return ""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for ch in DASH_CHARS:
        if ch in text:
            fail(rel, f"contains a long dash character (U+{ord(ch):04X})")
    if ATTRIBUTION.search(text):
        fail(rel, "contains an attribution string")
    return text


def main():
    names = sorted(x for x in os.listdir(NOTES_DIR) if not x.startswith(".")) if os.path.isdir(NOTES_DIR) else []
    for x in names:
        if not NOTE_FILE.match(x):
            fail(f"notes/{x}", "file name must be NNN-lowercase-slug.md")
    names = [x for x in names if NOTE_FILE.match(x)]
    nums = [note_number(x) for x in names]
    if len(set(nums)) != len(nums):
        fail("notes", "two notes share a number")
    if sorted(set(nums)) != list(range(1, len(set(nums)) + 1)):
        fail("notes", "note numbers must run 001, 002, 003 with no gaps")

    # which notes get the full checks
    has_origin = git("rev-parse", "--verify", "-q", "origin/main")[0] == 0
    changed = set()
    if has_origin:
        _, diff = git("diff", "--name-only", "origin/main")
        _, untracked = git("ls-files", "--others", "--exclude-standard")
        _, committed = git("diff", "--name-only", "origin/main...HEAD")
        changed = {p for p in (diff + untracked + committed).split("\n") if p.strip()}
        for p in sorted(changed):
            if not ALLOWED_CHANGES.match(p):
                fail(p, "this run may only change notes, checks, curriculum.md, README.md, glossary.md and data/shop.sql")
        full_notes = {os.path.basename(p) for p in changed if p.startswith("notes/")}
    else:
        infos.append("INFO no origin/main: full checks run on the newest note only, git checks skipped")
        full_notes = {names[-1]} if names else set()

    # notes whose curriculum box has a star, or is a capstone, need check yourself questions
    cur = scan_file("curriculum.md")
    quiz_needed, practice_notes = set(), set()
    for line in cur.split("\n"):
        m = re.match(r"^\s*- \[x\] (.*) \(note (\d{3})\)\s*$", line)
        if m and ("\u2605" in m.group(1) or m.group(1).startswith(("capstone:", "practice:"))):
            quiz_needed.add(int(m.group(2)))
        if m and m.group(1).startswith("practice:"):
            practice_notes.add(int(m.group(2)))

    for x in names:
        n = note_number(x)
        check_note(os.path.join(NOTES_DIR, x), names, x in full_notes, n in quiz_needed, n in practice_notes)

    # curriculum ticks match the notes
    for section in ("## THREAD", "## NOTES"):
        if section not in cur:
            fail("curriculum.md", f"missing the {section} section")
    ticked = []
    for line in cur.split("\n"):
        if re.match(r"^\s*- \[x\]", line):
            m = re.match(r"^\s*- \[x\] \S.* \(note (\d{3})\)\s*$", line)
            if not m:
                fail("curriculum.md", f"ticked box must end '(note NNN)': {line.strip()[:60]}")
            else:
                ticked.append(int(m.group(1)))
    if sorted(ticked) != sorted(nums):
        fail("curriculum.md", f"ticked boxes {sorted(ticked)} do not match the notes {sorted(nums)}")

    # README lists every note and the count
    readme = scan_file("README.md")
    for x in names:
        if f"(./notes/{x})" not in readme:
            fail("README.md", f"does not link ./notes/{x}")
    m = re.search(r"^notes so far: (\d+)$", readme, re.M)
    if not m or int(m.group(1)) != len(names):
        fail("README.md", f"needs a line 'notes so far: {len(names)}'")

    # glossary rows: term | meaning | link, sorted, links resolve
    gloss = scan_file("glossary.md")
    terms = []
    rows = [l for l in gloss.split("\n") if l.lstrip().startswith("|")]
    for row in rows[2:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) != 3:
            fail("glossary.md", f"row needs 3 cells: {row[:60]}")
            continue
        term, meaning, built = cells
        terms.append(term.lower())
        if len(meaning.split()) > 12:
            fail("glossary.md", f"meaning for '{term}' is over 12 words")
        links = LINK.findall(built)
        if not links:
            fail("glossary.md", f"'{term}' needs a link to the note that built it")
        for _, t in links:
            if not os.path.exists(os.path.normpath(os.path.join(ROOT, t))):
                fail("glossary.md", f"'{term}' links to a missing note: {t}")
    if terms != sorted(terms):
        fail("glossary.md", "terms must be in alphabetical order")
    if len(terms) != len(set(terms)):
        fail("glossary.md", "a term appears twice")
    scan_file("data/shop.sql")

    if has_origin:
        # shop.sql is append only
        _, d = git("diff", "origin/main", "--", "data/shop.sql")
        if any(l.startswith("-") and not l.startswith("---") for l in d.split("\n")):
            fail("data/shop.sql", "existing lines were changed or removed: append only")
        # old notes: only the footer line may change, unless every commit in this run is an audit fix
        _, subjects = git("log", "origin/main..HEAD", "--format=%s")
        subjects = [x for x in subjects.split("\n") if x.strip()]
        audit_run = bool(subjects) and all(x.startswith("audit ") for x in subjects)
        for p in ([] if audit_run else sorted(changed)):
            if not p.startswith("notes/") or git("cat-file", "-e", f"origin/main:{p}")[0] != 0:
                continue
            _, d = git("diff", "origin/main", "--", p)
            for l in d.split("\n"):
                if l.startswith(("+++", "---", "@@")) or not l.startswith(("+", "-")):
                    continue
                if not l[1:].startswith("prev:"):
                    fail(p, "an old note changed beyond its footer line")
                    break
        # commit messages
        _, log = git("log", "origin/main..HEAD", "--format=%B%x1e")
        for msg in [m.strip() for m in log.split("\x1e") if m.strip()]:
            subject = msg.split("\n")[0]
            if not COMMIT_SUBJECT.match(subject):
                fail("commits", f"subject does not match the formats: '{subject}'")
            if COMMIT_ATTRIBUTION.search(msg):
                fail("commits", f"commit '{subject}' carries an attribution line")

    for line in infos:
        print(line)
    for line in fails:
        print(line)
    print("PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
