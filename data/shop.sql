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
