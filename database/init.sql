PRAGMA foreign_keys = OFF;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS pickup_points;
DROP TABLE IF EXISTS order_statuses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS manufacturers;
DROP TABLE IF EXISTS suppliers;

CREATE TABLE roles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, role_id INTEGER NOT NULL REFERENCES roles(id), full_name TEXT NOT NULL, login TEXT NOT NULL UNIQUE, password TEXT NOT NULL);
CREATE TABLE suppliers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE manufacturers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
    manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    discount_percent INTEGER NOT NULL DEFAULT 0 CHECK(discount_percent BETWEEN 0 AND 100),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
    description TEXT NOT NULL DEFAULT '',
    image_path TEXT
);
CREATE TABLE pickup_points (id INTEGER PRIMARY KEY AUTOINCREMENT, address TEXT NOT NULL UNIQUE);
CREATE TABLE order_statuses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number INTEGER NOT NULL UNIQUE,
    article_summary TEXT NOT NULL,
    status_id INTEGER NOT NULL REFERENCES order_statuses(id),
    pickup_point_id INTEGER NOT NULL REFERENCES pickup_points(id),
    order_date TEXT,
    delivery_date TEXT,
    customer_name TEXT NOT NULL,
    pickup_code TEXT
);
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    UNIQUE(order_id, product_id)
);
CREATE INDEX idx_products_supplier_id ON products(supplier_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_stock_quantity ON products(stock_quantity);
CREATE INDEX idx_orders_status_id ON orders(status_id);

INSERT INTO roles(name) VALUES ('Авторизированный клиент');
INSERT INTO roles(name) VALUES ('Администратор');
INSERT INTO roles(name) VALUES ('Менеджер');
INSERT INTO suppliers(name) VALUES ('Kari');
INSERT INTO suppliers(name) VALUES ('Обувь для вас');
INSERT INTO manufacturers(name) VALUES ('Alessio Nesca');
INSERT INTO manufacturers(name) VALUES ('CROSBY');
INSERT INTO manufacturers(name) VALUES ('Kari');
INSERT INTO manufacturers(name) VALUES ('Marco Tozzi');
INSERT INTO manufacturers(name) VALUES ('Rieker');
INSERT INTO manufacturers(name) VALUES ('Рос');
INSERT INTO categories(name) VALUES ('Женская обувь');
INSERT INTO categories(name) VALUES ('Мужская обувь');
INSERT INTO pickup_points(address) VALUES ('420151, г. Лесной, ул. Вишневая, 32');
INSERT INTO pickup_points(address) VALUES ('125061, г. Лесной, ул. Подгорная, 8');
INSERT INTO pickup_points(address) VALUES ('630370, г. Лесной, ул. Шоссейная, 24');
INSERT INTO pickup_points(address) VALUES ('400562, г. Лесной, ул. Зеленая, 32');
INSERT INTO pickup_points(address) VALUES ('614510, г. Лесной, ул. Маяковского, 47');
INSERT INTO pickup_points(address) VALUES ('410542, г. Лесной, ул. Светлая, 46');
INSERT INTO pickup_points(address) VALUES ('620839, г. Лесной, ул. Цветочная, 8');
INSERT INTO pickup_points(address) VALUES ('443890, г. Лесной, ул. Коммунистическая, 1');
INSERT INTO pickup_points(address) VALUES ('603379, г. Лесной, ул. Спортивная, 46');
INSERT INTO pickup_points(address) VALUES ('603721, г. Лесной, ул. Гоголя, 41');
INSERT INTO pickup_points(address) VALUES ('410172, г. Лесной, ул. Северная, 13');
INSERT INTO pickup_points(address) VALUES ('614611, г. Лесной, ул. Молодежная, 50');
INSERT INTO pickup_points(address) VALUES ('454311, г.Лесной, ул. Новая, 19');
INSERT INTO pickup_points(address) VALUES ('660007, г.Лесной, ул. Октябрьская, 19');
INSERT INTO pickup_points(address) VALUES ('603036, г. Лесной, ул. Садовая, 4');
INSERT INTO pickup_points(address) VALUES ('394060, г.Лесной, ул. Фрунзе, 43');
INSERT INTO pickup_points(address) VALUES ('410661, г. Лесной, ул. Школьная, 50');
INSERT INTO pickup_points(address) VALUES ('625590, г. Лесной, ул. Коммунистическая, 20');
INSERT INTO pickup_points(address) VALUES ('625683, г. Лесной, ул. 8 Марта');
INSERT INTO pickup_points(address) VALUES ('450983, г.Лесной, ул. Комсомольская, 26');
INSERT INTO pickup_points(address) VALUES ('394782, г. Лесной, ул. Чехова, 3');
INSERT INTO pickup_points(address) VALUES ('603002, г. Лесной, ул. Дзержинского, 28');
INSERT INTO pickup_points(address) VALUES ('450558, г. Лесной, ул. Набережная, 30');
INSERT INTO pickup_points(address) VALUES ('344288, г. Лесной, ул. Чехова, 1');
INSERT INTO pickup_points(address) VALUES ('614164, г.Лесной,  ул. Степная, 30');
INSERT INTO pickup_points(address) VALUES ('394242, г. Лесной, ул. Коммунистическая, 43');
INSERT INTO pickup_points(address) VALUES ('660540, г. Лесной, ул. Солнечная, 25');
INSERT INTO pickup_points(address) VALUES ('125837, г. Лесной, ул. Шоссейная, 40');
INSERT INTO pickup_points(address) VALUES ('125703, г. Лесной, ул. Партизанская, 49');
INSERT INTO pickup_points(address) VALUES ('625283, г. Лесной, ул. Победы, 46');
INSERT INTO pickup_points(address) VALUES ('614753, г. Лесной, ул. Полевая, 35');
INSERT INTO pickup_points(address) VALUES ('426030, г. Лесной, ул. Маяковского, 44');
INSERT INTO pickup_points(address) VALUES ('450375, г. Лесной ул. Клубная, 44');
INSERT INTO pickup_points(address) VALUES ('625560, г. Лесной, ул. Некрасова, 12');
INSERT INTO pickup_points(address) VALUES ('630201, г. Лесной, ул. Комсомольская, 17');
INSERT INTO pickup_points(address) VALUES ('190949, г. Лесной, ул. Мичурина, 26');
INSERT INTO order_statuses(name) VALUES ('Завершен');
INSERT INTO order_statuses(name) VALUES ('Новый');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Администратор'), 'Никифорова Весения Николаевна', '94d5ous@gmail.com', 'uzWC67');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Администратор'), 'Сазонов Руслан Германович', 'uth4iz@mail.com', '2L6KZG');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Администратор'), 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Менеджер'), 'Степанов Михаил Артёмович', '1diph5e@tutanota.com', '8ntwUp');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Менеджер'), 'Ворсин Петр Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Менеджер'), 'Старикова Елена Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Авторизированный клиент'), 'Михайлюк Анна Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Авторизированный клиент'), 'Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Авторизированный клиент'), 'Ворсин Петр Евгеньевич', '1qz4kw@mail.com', 'gynQMT');
INSERT INTO users(role_id, full_name, login, password) VALUES ((SELECT id FROM roles WHERE name='Авторизированный клиент'), 'Старикова Елена Павловна', '4np6se@mail.com', 'AtnDjr');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('А112Т4', 'Ботинки', 'шт.', 4990.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 3, 6, 'Женские Ботинки демисезонные kari', 'images/1.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('F635R4', 'Ботинки', 'шт.', 3244.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Marco Tozzi'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 13, 'Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый', 'images/2.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('H782T5', 'Туфли', 'шт.', 4499.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Мужская обувь'), 4, 5, 'Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный', 'images/3.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('G783F5', 'Ботинки', 'шт.', 5900.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Рос'), (SELECT id FROM categories WHERE name='Мужская обувь'), 2, 8, 'Мужские ботинки Рос-Обувь кожаные с натуральным мехом', 'images/4.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('J384T6', 'Ботинки', 'шт.', 3800.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Мужская обувь'), 2, 16, 'B3430/14 Полуботинки мужские Rieker', 'images/5.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('D572U8', 'Кроссовки', 'шт.', 4100.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Рос'), (SELECT id FROM categories WHERE name='Мужская обувь'), 3, 6, '129615-4 Кроссовки мужские', 'images/6.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('F572H7', 'Туфли', 'шт.', 2700.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Marco Tozzi'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 14, 'Туфли Marco Tozzi женские летние, размер 39, цвет черный', 'images/7.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('D329H3', 'Полуботинки', 'шт.', 1890.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Alessio Nesca'), (SELECT id FROM categories WHERE name='Женская обувь'), 4, 4, 'Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый', 'images/8.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('B320R5', 'Туфли', 'шт.', 4300.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 6, 'Туфли Rieker женские демисезонные, размер 41, цвет коричневый', 'images/9.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('G432E4', 'Туфли', 'шт.', 2800.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 3, 15, 'Туфли kari женские TR-YR-413017, размер 37, цвет: черный', 'images/10.jpg');
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('S213E3', 'Полуботинки', 'шт.', 2156.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Мужская обувь'), 3, 6, '407700/01-01 Полуботинки мужские CROSBY', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('E482R4', 'Полуботинки', 'шт.', 1800.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 14, 'Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('S634B5', 'Кеды', 'шт.', 5500.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Мужская обувь'), 3, 0, 'Кеды Caprice мужские демисезонные, размер 42, цвет черный', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('K345R4', 'Полуботинки', 'шт.', 2100.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Мужская обувь'), 2, 3, '407700/01-02 Полуботинки мужские CROSBY', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('O754F4', 'Туфли', 'шт.', 5400.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Женская обувь'), 4, 18, 'Туфли женские демисезонные Rieker артикул 55073-68/37', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('G531F4', 'Ботинки', 'шт.', 6600.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 12, 9, 'Ботинки женские зимние ROMER арт. 893167-01 Черный', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('J542F5', 'Тапочки', 'шт.', 500.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Мужская обувь'), 13, 0, 'Тапочки мужские Арт.70701-55-67син р.41', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('B431R5', 'Ботинки', 'шт.', 2700.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Мужская обувь'), 2, 5, 'Мужские кожаные ботинки/мужские ботинки', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('P764G4', 'Туфли', 'шт.', 6800.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Женская обувь'), 15, 15, 'Туфли женские, ARGO, размер 38', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('C436G5', 'Ботинки', 'шт.', 10200.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Alessio Nesca'), (SELECT id FROM categories WHERE name='Женская обувь'), 15, 9, 'Ботинки женские, ARGO, размер 40', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('F427R5', 'Ботинки', 'шт.', 11800.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Женская обувь'), 15, 11, 'Ботинки на молнии с декоративной пряжкой FRAU', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('N457T5', 'Полуботинки', 'шт.', 4600.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Женская обувь'), 3, 13, 'Полуботинки Ботинки черные зимние, мех', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('D364R4', 'Туфли', 'шт.', 12400.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 16, 5, 'Туфли Luiza Belly женские Kate-lazo черные из натуральной замши', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('S326R5', 'Тапочки', 'шт.', 9900.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Мужская обувь'), 17, 15, 'Мужские кожаные тапочки "Профиль С.Дали"', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('L754R4', 'Полуботинки', 'шт.', 1700.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Kari'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 7, 'Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('M542T5', 'Кроссовки', 'шт.', 2800.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Мужская обувь'), 18, 3, 'Кроссовки мужские TOFA', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('D268G5', 'Туфли', 'шт.', 4399.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Женская обувь'), 3, 12, 'Туфли Rieker женские демисезонные, размер 36, цвет коричневый', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('T324F5', 'Сапоги', 'шт.', 4699.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='CROSBY'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 5, 'Сапоги замша Цвет: синий', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('K358H6', 'Тапочки', 'шт.', 599.0, (SELECT id FROM suppliers WHERE name='Kari'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Мужская обувь'), 20, 2, 'Тапочки мужские син р.41', NULL);
INSERT INTO products(article, name, unit, price, supplier_id, manufacturer_id, category_id, discount_percent, stock_quantity, description, image_path) VALUES ('H535R5', 'Ботинки', 'шт.', 2300.0, (SELECT id FROM suppliers WHERE name='Обувь для вас'), (SELECT id FROM manufacturers WHERE name='Rieker'), (SELECT id FROM categories WHERE name='Женская обувь'), 2, 7, 'Женские Ботинки демисезонные', NULL);
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (1, 'А112Т4, 2, F635R4, 2', (SELECT id FROM order_statuses WHERE name='Завершен'), 1, '2025-02-27', '2025-04-20', 'Степанов Михаил Артёмович', '901');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (2, 'H782T5, 1, G783F5, 1', (SELECT id FROM order_statuses WHERE name='Завершен'), 11, '2022-09-28', '2025-04-21', 'Никифорова Весения Николаевна', '902');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (3, 'J384T6, 10, D572U8, 10', (SELECT id FROM order_statuses WHERE name='Завершен'), 2, '2025-03-21', '2025-04-22', 'Сазонов Руслан Германович', '903');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (4, 'F572H7, 5, D329H3, 4', (SELECT id FROM order_statuses WHERE name='Завершен'), 11, '2025-02-20', '2025-04-23', 'Одинцов Серафим Артёмович', '904');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (5, 'А112Т4, 2, F635R4, 2', (SELECT id FROM order_statuses WHERE name='Завершен'), 2, '2025-03-17', '2025-04-24', 'Степанов Михаил Артёмович', '905');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (6, 'H782T5, 1, G783F5, 1', (SELECT id FROM order_statuses WHERE name='Завершен'), 15, '2025-03-01', '2025-04-25', 'Никифорова Весения Николаевна', '906');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (7, 'J384T6, 10, D572U8, 10', (SELECT id FROM order_statuses WHERE name='Завершен'), 3, '2025-02-28', '2025-04-26', 'Сазонов Руслан Германович', '907');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (8, 'F572H7, 5, D329H3, 4', (SELECT id FROM order_statuses WHERE name='Новый'), 19, '2025-03-31', '2025-04-27', 'Одинцов Серафим Артёмович', '908');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (9, 'B320R5, 5, G432E4, 1', (SELECT id FROM order_statuses WHERE name='Новый'), 5, '2025-04-02', '2025-04-28', 'Степанов Михаил Артёмович', '909');
INSERT INTO orders(order_number, article_summary, status_id, pickup_point_id, order_date, delivery_date, customer_name, pickup_code) VALUES (10, 'S213E3, 5, E482R4, 5', (SELECT id FROM order_statuses WHERE name='Новый'), 19, '2025-04-03', '2025-04-29', 'Степанов Михаил Артёмович', '910');
INSERT INTO order_items(order_id, product_id, quantity) VALUES (1, 1, 2);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (1, 2, 2);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (2, 3, 1);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (2, 4, 1);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (3, 5, 10);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (3, 6, 10);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (4, 7, 5);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (4, 8, 4);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (5, 1, 2);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (5, 2, 2);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (6, 3, 1);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (6, 4, 1);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (7, 5, 10);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (7, 6, 10);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (8, 7, 5);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (8, 8, 4);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (9, 9, 5);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (9, 10, 1);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (10, 11, 5);
INSERT INTO order_items(order_id, product_id, quantity) VALUES (10, 12, 5);
PRAGMA foreign_keys = ON;