# 074: YAML traps, when no means false
builds on: [067 JSON types, strings, numbers, booleans, null, objects and arrays](./067-json-types.md), [073 YAML, indentation as structure](./073-yaml.md)
section: giving data a shape, part 14, ~2 min read

i wrote `gift_wrap: no` in a config file and the program that read it got False. i never wrote False, so who decided that?

the parser did. in [YAML](./073-yaml.md), the text format where indentation shows nesting, values usually have no quotes, so the program that reads the file (a parser) has to decide what each bare word, one with no quotes, is: text, a number, or a [boolean](./067-json-types.md), a true or false value? the older YAML rules, 1.1, say yes, no, on and off are booleans. PyYAML, the python library that reads YAML, still follows them (Yes and ON too, not y or n). here is each line read on its own, with what python gets back, using the shop (the imaginary gujarati snack store these notes run on). order 102 had the note "no nuts", and gift_wrap is a flag i made up:

```python
import yaml  # PyYAML, a library that reads YAML text
lines = ["note: no nuts", "gift_wrap: no", 'gift_wrap: "no"', "gift_wrap: on", "order_id: 102", 'order_id: "102"']
for line in lines:
    value = list(yaml.safe_load(line).values())[0]  # safe_load turns YAML text into python values
    print(line, "|", type(value).__name__, repr(value))
```

```output
note: no nuts | str 'no nuts'
gift_wrap: no | bool False
gift_wrap: "no" | str 'no'
gift_wrap: on | bool True
order_id: 102 | int 102
order_id: "102" | str '102'
```

"no nuts" stays text because only the word on its own flips. quotes are the fix: "no" in quotes is text, same as "102" in quotes stops being a number.

i assumed a bare word was just a word, and the parser reads it and decides. a country code of NO for Norway comes back as False the same way (i ran it).

the 1.2 spec only treats true and false (also True, TRUE) as booleans, so what you get depends on which parser reads the file. quote anything that must stay text.

### check yourself

1. a settings file says `lights: Off` and PyYAML reads it. what does the program get, and what one change keeps it as text?
<details><summary>answer</summary>

False, a boolean, because Off in any capitalization is a 1.1 boolean word. writing `lights: "Off"` keeps the text Off. the tempting answer is the text Off, from thinking only lowercase words count.

</details>

2. Disha ordered 105 with the note "gift, please wrap", so a script writes `gift_wrap: yes`. one program reads it with PyYAML, another with a parser that follows the 1.2 rules. what does each see?
<details><summary>answer</summary>

PyYAML sees True. a parser that follows the 1.2 rules sees the text yes, since only true and false are booleans there. the tempting answer is True for both, from thinking the file means one thing.

</details>

---
prev: [073 YAML, indentation as structure](./073-yaml.md) | next: not written yet
