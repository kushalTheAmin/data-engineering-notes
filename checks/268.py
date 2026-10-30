# checks for notes/268-capstone-modeling-product-reviews-for-the-shop.md
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _shop import shop
q = lambda con, s: con.execute(s).fetchall()
DDL = """CREATE TABLE reviews (
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    product_id  INTEGER NOT NULL REFERENCES products (product_id),
    rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    body        VARCHAR,
    created_at  TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP NOT NULL,
    deleted_at  TIMESTAMP,
    PRIMARY KEY (customer_id, product_id)
)"""
ROWS = """INSERT INTO reviews VALUES
    (1, 1, 5, 'soft and fresh',  TIMESTAMP '2026-04-12 10:00:00', TIMESTAMP '2026-04-12 10:00:00', NULL),
    (2, 1, 4, 'a bit dry',       TIMESTAMP '2026-04-12 11:00:00', TIMESTAMP '2026-04-12 11:00:00', NULL),
    (3, 1, 2, 'changed my mind', TIMESTAMP '2026-04-13 09:00:00', TIMESTAMP '2026-04-14 09:00:00', TIMESTAMP '2026-04-14 09:00:00'),
    (1, 2, 3, 'ok',              TIMESTAMP '2026-04-13 12:00:00', TIMESTAMP '2026-04-13 12:00:00', NULL)"""
con = shop()
con.execute(DDL); con.execute(ROWS)
# ids used: Asha 1, Bhavin 2, Chirag 3, dhokla 1, khandvi 2, fafda 6
assert q(con, "SELECT customer_id, name FROM customers WHERE customer_id <= 3") == [(1, 'Asha'), (2, 'Bhavin'), (3, 'Chirag')]
assert q(con, "SELECT product_id, name FROM products WHERE product_id IN (1, 2, 6) ORDER BY 1") == [(1, 'dhokla'), (2, 'khandvi'), (6, 'fafda')]
# main result: live reviews only
assert q(con, "SELECT p.name, count(*), avg(r.rating) FROM reviews r JOIN products p ON p.product_id = r.product_id WHERE r.deleted_at IS NULL GROUP BY p.name ORDER BY p.name") == [('dhokla', 2, 4.5), ('khandvi', 1, 3.0)]
# question 2: no filter, 5 + 4 + 2 over 3
assert q(con, "SELECT count(*), round(avg(rating), 2) FROM reviews WHERE product_id = 1") == [(3, 3.67)]
assert round((5 + 4 + 2) / 3, 2) == 3.67
# question 1: the soft deleted pair is still taken
try:
    con.execute("INSERT INTO reviews VALUES (3, 1, 4, 'again', TIMESTAMP '2026-04-15 09:00:00', TIMESTAMP '2026-04-15 09:00:00', NULL)")
    raise SystemExit("should have failed")
except Exception as e:
    assert "onstraint" in type(e).__name__ or "onstraint" in str(e)
con.execute("UPDATE reviews SET rating = 4, deleted_at = NULL, updated_at = TIMESTAMP '2026-04-15 09:00:00' WHERE customer_id = 3 AND product_id = 1")
assert q(con, "SELECT count(*) FROM reviews WHERE deleted_at IS NULL") == [(4,)]
# CHECK refuses a 6
try:
    con.execute("INSERT INTO reviews VALUES (5, 6, 6, NULL, TIMESTAMP '2026-04-15 09:00:00', TIMESTAMP '2026-04-15 09:00:00', NULL)")
    raise SystemExit("should have failed")
except Exception as e:
    assert "onstraint" in type(e).__name__ or "onstraint" in str(e)
# the folder claim: DuckDB refuses a foreign key across schemas
c2 = shop()
c2.execute("CREATE SCHEMA feedback")
try:
    c2.execute("CREATE TABLE feedback.reviews (customer_id INTEGER REFERENCES customers (customer_id))")
    raise SystemExit("should have failed")
except Exception as e:
    assert "across different schemas" in str(e)
# the last 14 notes of the section are 254 to 267
assert len(range(254, 268)) == 14
# the shop notes 103, 104 and 112 call fafda a crunchy chickpea flour snack, so 268 uses the same name (gram flour is the same flour, but unglossed)
