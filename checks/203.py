# checks for notes/203-recursive-ctes-following-a-chain-of-rows.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
REC = "WITH RECURSIVE chain AS (SELECT customer_id, name, 0 AS depth FROM customers WHERE name = '{n}' UNION ALL SELECT cu.customer_id, cu.name, ch.depth + 1 FROM chain AS ch JOIN referrals AS r ON r.referred_by = ch.customer_id JOIN customers AS cu ON cu.customer_id = r.customer_id) SELECT name, depth FROM chain ORDER BY depth, name"
# referrals: 4 rows, Bhavin and Chirag from Asha, Disha from Bhavin, Esha from Disha
names = dict(q("SELECT customer_id, name FROM customers"))
refs = {(names[c], names[b]) for c, b in q("SELECT customer_id, referred_by FROM referrals")}
assert refs == {("Bhavin", "Asha"), ("Chirag", "Asha"), ("Disha", "Bhavin"), ("Esha", "Disha")}
# the round table, in python: a while loop that ends on an empty list
found, frontier, rounds = [], ["Asha"], []
while frontier:
    rounds.append(frontier)
    found += frontier
    frontier = sorted(c for c, b in refs if b in rounds[-1])
assert rounds == [["Asha"], ["Bhavin", "Chirag"], ["Disha"], ["Esha"]]
assert frontier == []  # round 4 finds nobody, so stop
# main query
assert q(REC.format(n="Asha")) == [("Asha", 0), ("Bhavin", 1), ("Chirag", 1), ("Disha", 2), ("Esha", 3)]
# depth is the old depth plus 1 per round
assert [d for _, d in q(REC.format(n="Asha"))] == [0, 1, 1, 2, 3]
# nobody was referred by Esha
assert q("SELECT count(*) FROM referrals WHERE referred_by = 5") == [(0,)]
# source: https://www.postgresql.org/docs/current/queries-with.html
#   confirmed: recursive WITH is a non-recursive term, UNION or UNION ALL, then a recursive term that alone refers to the query's own output;
#   each iteration substitutes the working table (previous round) for the self reference;
#   "be sure that the recursive part of the query will eventually return no tuples, or else the query will loop indefinitely";
#   (the docs also give a sub-parts example, not used in the note)
