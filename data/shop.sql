-- the shop: an imaginary online store that sells gujarati snacks
-- this is the running example for every note in this repo
-- rule: never edit or delete a line in this file. new tables get appended at the end,
-- and existing tables never get new rows, so every number an old note shows stays true

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        VARCHAR NOT NULL,
    city        VARCHAR,
    joined_on   DATE NOT NULL
);

INSERT INTO customers VALUES
    (1, 'Asha',   'Jersey City', DATE '2026-01-05'),
    (2, 'Bhavin', 'Edison',      DATE '2026-01-20'),
    (3, 'Chirag', 'Jersey City', DATE '2026-02-11'),
    (4, 'Disha',  'Hoboken',     DATE '2026-03-02'),
    (5, 'Esha',   NULL,          DATE '2026-03-15');

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       VARCHAR NOT NULL,
    category   VARCHAR NOT NULL,
    price      DECIMAL(6, 2) NOT NULL
);

INSERT INTO products VALUES
    (1, 'dhokla',      'snack', 6.00),
    (2, 'khandvi',     'snack', 7.50),
    (3, 'jalebi',      'sweet', 5.00),
    (4, 'kaju katli',  'sweet', 12.00),
    (5, 'masala chai', 'drink', 3.00),
    (6, 'fafda',       'snack', 4.50);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
    ordered_at  TIMESTAMP NOT NULL,
    status      VARCHAR NOT NULL
);

INSERT INTO orders VALUES
    (101, 1, TIMESTAMP '2026-04-01 09:15:00', 'delivered'),
    (102, 2, TIMESTAMP '2026-04-01 18:40:00', 'delivered'),
    (103, 1, TIMESTAMP '2026-04-03 12:05:00', 'delivered'),
    (104, 3, TIMESTAMP '2026-04-04 08:30:00', 'cancelled'),
    (105, 4, TIMESTAMP '2026-04-06 19:10:00', 'delivered'),
    (106, 1, TIMESTAMP '2026-04-08 10:00:00', 'pending'),
    (107, 2, TIMESTAMP '2026-04-09 13:45:00', 'delivered');

CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders (order_id),
    product_id INTEGER NOT NULL REFERENCES products (product_id),
    quantity   INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO order_items VALUES
    (101, 1, 2), (101, 5, 2),
    (102, 3, 1), (102, 4, 1),
    (103, 2, 1), (103, 5, 1),
    (104, 1, 3),
    (105, 4, 2), (105, 3, 2), (105, 5, 1),
    (106, 2, 2),
    (107, 1, 1), (107, 3, 1);

-- added by note 032: star ratings for delivered orders, kept two ways.
-- stars leaves unrated orders NULL, stars_zero_filled stores 0 for them
CREATE TABLE order_ratings (
    order_id          INTEGER NOT NULL REFERENCES orders (order_id),
    stars             INTEGER,
    stars_zero_filled INTEGER NOT NULL
);

INSERT INTO order_ratings VALUES
    (101, 5,    5),
    (102, 4,    4),
    (103, NULL, 0),
    (105, 3,    3),
    (107, NULL, 0);

-- added by note 063: short notes customers left on an order, some with commas inside
CREATE TABLE order_notes (
    order_id INTEGER NOT NULL REFERENCES orders (order_id),
    note     VARCHAR NOT NULL
);

INSERT INTO order_notes VALUES
    (101, 'extra chutney, less spicy'),
    (102, 'no nuts'),
    (105, 'gift, please wrap');

-- added by note 064: delivery messages, one with a quote mark and one with a newline inside
CREATE TABLE order_messages (
    order_id INTEGER NOT NULL REFERENCES orders (order_id),
    message  VARCHAR NOT NULL
);

INSERT INTO order_messages VALUES
    (103, 'less sweet'),
    (106, 'the "extra crispy" fafda please'),
    (107, 'call first' || chr(10) || 'leave at the door');

-- added by note 124: names exactly as typed into the signup form, stray spaces and capitals included
CREATE TABLE signups (
    signup_id  INTEGER PRIMARY KEY,
    typed_name VARCHAR NOT NULL
);

INSERT INTO signups VALUES
    (1, 'Asha'),
    (2, 'bhavin '),
    (3, 'CHIRAG '),
    (4, 'Disha');

-- added by note 130: orders placed and cancelled per day, april 1 to 9, counted from orders. april 2, 5 and 7 had no orders
CREATE TABLE daily_orders (
    day       DATE PRIMARY KEY,
    placed    INTEGER NOT NULL,
    cancelled INTEGER NOT NULL
);

INSERT INTO daily_orders VALUES
    (DATE '2026-04-01', 2, 0),
    (DATE '2026-04-02', 0, 0),
    (DATE '2026-04-03', 1, 0),
    (DATE '2026-04-04', 1, 1),
    (DATE '2026-04-05', 0, 0),
    (DATE '2026-04-06', 1, 0),
    (DATE '2026-04-07', 0, 0),
    (DATE '2026-04-08', 1, 0),
    (DATE '2026-04-09', 1, 0);

-- added by note 133: a supplier price list typed by hand as text. jalebi says n/a, kaju katli uses a comma as the decimal mark
CREATE TABLE price_export (
    product_id INTEGER PRIMARY KEY,
    name       VARCHAR NOT NULL,
    price_text VARCHAR NOT NULL
);

INSERT INTO price_export VALUES
    (1, 'dhokla',      '6.00'),
    (2, 'khandvi',     '7.50'),
    (3, 'jalebi',      'n/a'),
    (4, 'kaju katli',  '12,00'),
    (5, 'masala chai', '3.00');

-- added by note 165: a flat delivery fee per order, one row per order. cancelled order 104 was never delivered, so its fee is 0.00
CREATE TABLE order_fees (
    order_id INTEGER PRIMARY KEY REFERENCES orders (order_id),
    fee      DECIMAL(4, 2) NOT NULL
);

INSERT INTO order_fees VALUES
    (101, 2.00),
    (102, 3.00),
    (103, 2.00),
    (104, 0.00),
    (105, 3.00),
    (106, 2.00),
    (107, 3.00);

-- added by note 166: a delivery zone per city. the last row has a NULL city, a catch-all for addresses nobody filled in
CREATE TABLE delivery_zones (
    city VARCHAR,
    zone VARCHAR NOT NULL
);

INSERT INTO delivery_zones VALUES
    ('Jersey City', 'north'),
    ('Edison',      'south'),
    ('Hoboken',     'north'),
    (NULL,          'unassigned');
