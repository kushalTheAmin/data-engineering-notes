# checks for notes/219-sequences-where-made-up-ids-come-from.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
con = shop()
q = lambda s: con.execute(s).fetchall()
con.execute("CREATE SEQUENCE ticket_id START 1")
con.execute("CREATE TABLE tickets (ticket_id INTEGER PRIMARY KEY DEFAULT nextval('ticket_id'), customer VARCHAR NOT NULL)")
con.execute("INSERT INTO tickets (customer) VALUES ('Asha'), ('Bhavin')")
try:
    con.execute("INSERT INTO tickets (customer) VALUES (NULL)")
    assert False
except Exception as e:
    assert "not null" in str(e).lower()
con.execute("INSERT INTO tickets (customer) VALUES ('Chirag')")
# the refused insert still used 3, so Chirag is 4
assert q("SELECT * FROM tickets ORDER BY ticket_id") == [(1, "Asha"), (2, "Bhavin"), (4, "Chirag")]
# check yourself 1
con.execute("DELETE FROM tickets WHERE customer = 'Chirag'")
con.execute("INSERT INTO tickets (customer) VALUES ('Disha')")
assert q("SELECT ticket_id FROM tickets WHERE customer = 'Disha'") == [(5,)]
# check yourself 2
con.execute("CREATE SEQUENCE o START 1")
con.execute("CREATE TABLE orders2 (order_id INTEGER PRIMARY KEY DEFAULT nextval('o'), status VARCHAR)")
con.execute("INSERT INTO orders2 VALUES (101, 'delivered'), (102, 'delivered')")
con.execute("INSERT INTO orders2 (status) VALUES ('pending')")
assert q("SELECT order_id FROM orders2 WHERE status = 'pending'") == [(1,)]
# source: https://www.postgresql.org/docs/current/functions-sequence.html
#   confirmed (opened this run): nextval value is not reclaimed if the transaction aborts, so gaps; sequences cannot give gapless numbers.
# source: https://www.postgresql.org/docs/current/datatype-numeric.html
#   confirmed (opened this run): serial is a notational convenience built on a sequence plus DEFAULT nextval(...); gaps appear because a value is used up even if the row never lands.
#   also confirmed there: AUTO_INCREMENT is a similar property supported by some other databases.
# note: nextval is not undone by ROLLBACK in DuckDB, checked by running it in python this run.
con.execute("CREATE SEQUENCE rb START 1")
con.execute("BEGIN")
assert q("SELECT nextval('rb')") == [(1,)]
con.execute("ROLLBACK")
assert q("SELECT nextval('rb')") == [(2,)]
# source: https://dev.mysql.com/doc/refman/8.4/en/example-auto-increment.html
#   confirmed (opened this run): "When you insert any other value into an AUTO_INCREMENT column, the column is set to that value and the sequence is reset so that the next automatically generated value follows sequentially from the largest column value", so after 101 and 102 typed by hand MySQL hands out 103
# the gloss for transaction in the note: a ROLLBACK undoes the changes made since BEGIN, but not nextval (asserted above)
con.execute("CREATE TABLE tx (a INTEGER)")
con.execute("BEGIN")
con.execute("INSERT INTO tx VALUES (1)")
con.execute("ROLLBACK")
assert q("SELECT count(*) FROM tx") == [(0,)]
