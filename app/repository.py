from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from .models import Order, Product, User


class Repository:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON;')
        return connection

    def authenticate(self, login: str, password: str) -> User | None:
        query = """
            SELECT u.id, u.full_name, u.login, u.password, r.name AS role
            FROM users u
            JOIN roles r ON r.id = u.role_id
            WHERE u.login = ? AND u.password = ?
        """
        with self.connect() as connection:
            row = connection.execute(query, (login.strip(), password.strip())).fetchone()
        if row is None:
            return None
        return User(
            id=row['id'],
            full_name=row['full_name'],
            login=row['login'],
            password=row['password'],
            role=row['role'],
        )

    def get_suppliers(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute('SELECT name FROM suppliers ORDER BY name').fetchall()
        return [row['name'] for row in rows]

    def get_categories(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute('SELECT name FROM categories ORDER BY name').fetchall()
        return [row['name'] for row in rows]

    def get_manufacturers(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute('SELECT name FROM manufacturers ORDER BY name').fetchall()
        return [row['name'] for row in rows]

    def get_statuses(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute('SELECT name FROM order_statuses ORDER BY name').fetchall()
        return [row['name'] for row in rows]

    def get_pickup_points(self) -> list[str]:
        with self.connect() as connection:
            rows = connection.execute(
                'SELECT address FROM pickup_points ORDER BY address'
            ).fetchall()
        return [row['address'] for row in rows]

    def get_products(
        self,
        search_text: str = '',
        supplier_name: str = 'Все поставщики',
        sort_order: str = 'Без сортировки',
    ) -> list[Product]:
        query = """
            SELECT
                p.id,
                p.article,
                p.name,
                p.unit,
                p.price,
                s.id AS supplier_id,
                s.name AS supplier_name,
                m.id AS manufacturer_id,
                m.name AS manufacturer_name,
                c.id AS category_id,
                c.name AS category_name,
                p.discount_percent,
                p.stock_quantity,
                p.description,
                p.image_path
            FROM products p
            JOIN suppliers s ON s.id = p.supplier_id
            JOIN manufacturers m ON m.id = p.manufacturer_id
            JOIN categories c ON c.id = p.category_id
            WHERE 1 = 1
        """
        params: list[object] = []
        if search_text.strip():
            pattern = f'%{search_text.strip().lower()}%'
            query += """
                AND (
                    lower(p.article) LIKE ? OR
                    lower(p.name) LIKE ? OR
                    lower(p.unit) LIKE ? OR
                    lower(p.description) LIKE ? OR
                    lower(s.name) LIKE ? OR
                    lower(m.name) LIKE ? OR
                    lower(c.name) LIKE ?
                )
            """
            params.extend([pattern] * 7)
        if supplier_name != 'Все поставщики':
            query += ' AND s.name = ? '
            params.append(supplier_name)
        if sort_order == 'По количеству: возрастание':
            query += ' ORDER BY p.stock_quantity ASC, p.name ASC '
        elif sort_order == 'По количеству: убывание':
            query += ' ORDER BY p.stock_quantity DESC, p.name ASC '
        else:
            query += ' ORDER BY p.id ASC '

        with self.connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._map_product(row) for row in rows]

    def get_product_by_id(self, product_id: int) -> Product | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    p.id,
                    p.article,
                    p.name,
                    p.unit,
                    p.price,
                    s.id AS supplier_id,
                    s.name AS supplier_name,
                    m.id AS manufacturer_id,
                    m.name AS manufacturer_name,
                    c.id AS category_id,
                    c.name AS category_name,
                    p.discount_percent,
                    p.stock_quantity,
                    p.description,
                    p.image_path
                FROM products p
                JOIN suppliers s ON s.id = p.supplier_id
                JOIN manufacturers m ON m.id = p.manufacturer_id
                JOIN categories c ON c.id = p.category_id
                WHERE p.id = ?
                """,
                (product_id,),
            ).fetchone()
        if row is None:
            return None
        return self._map_product(row)

    def get_next_product_id(self) -> int:
        with self.connect() as connection:
            value = connection.execute(
                'SELECT COALESCE(MAX(id), 0) + 1 AS next_id FROM products'
            ).fetchone()['next_id']
        return int(value)

    def get_next_order_number(self) -> int:
        with self.connect() as connection:
            value = connection.execute(
                'SELECT COALESCE(MAX(order_number), 0) + 1 AS next_id FROM orders'
            ).fetchone()['next_id']
        return int(value)

    def save_product(self, data: dict[str, object], product_id: int | None = None) -> None:
        supplier_id = self._get_or_create_lookup_id('suppliers', str(data['supplier_name']))
        manufacturer_id = self._get_or_create_lookup_id(
            'manufacturers', str(data['manufacturer_name'])
        )
        category_id = self._get_or_create_lookup_id('categories', str(data['category_name']))
        payload = (
            str(data['article']).strip(),
            str(data['name']).strip(),
            str(data['unit']).strip(),
            float(data['price']),
            supplier_id,
            manufacturer_id,
            category_id,
            int(data['discount_percent']),
            int(data['stock_quantity']),
            str(data['description']).strip(),
            str(data['image_path']).strip() if data.get('image_path') else None,
        )
        with self.connect() as connection:
            if product_id is None:
                connection.execute(
                    """
                    INSERT INTO products (
                        article, name, unit, price, supplier_id, manufacturer_id,
                        category_id, discount_percent, stock_quantity, description, image_path
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    payload,
                )
            else:
                connection.execute(
                    """
                    UPDATE products
                    SET article = ?,
                        name = ?,
                        unit = ?,
                        price = ?,
                        supplier_id = ?,
                        manufacturer_id = ?,
                        category_id = ?,
                        discount_percent = ?,
                        stock_quantity = ?,
                        description = ?,
                        image_path = ?
                    WHERE id = ?
                    """,
                    (*payload, product_id),
                )

    def can_delete_product(self, product_id: int) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                'SELECT COUNT(*) AS cnt FROM order_items WHERE product_id = ?',
                (product_id,),
            ).fetchone()
        return int(row['cnt']) == 0

    def delete_product(self, product_id: int) -> None:
        with self.connect() as connection:
            connection.execute('DELETE FROM products WHERE id = ?', (product_id,))

    def get_orders(self) -> list[Order]:
        query = """
            SELECT
                o.id,
                o.order_number,
                o.article_summary,
                os.id AS status_id,
                os.name AS status_name,
                pp.id AS pickup_point_id,
                pp.address AS pickup_address,
                o.order_date,
                o.delivery_date,
                o.customer_name,
                o.pickup_code
            FROM orders o
            JOIN order_statuses os ON os.id = o.status_id
            JOIN pickup_points pp ON pp.id = o.pickup_point_id
            ORDER BY o.order_number ASC
        """
        with self.connect() as connection:
            rows = connection.execute(query).fetchall()
        return [self._map_order(row) for row in rows]

    def get_order_by_id(self, order_id: int) -> Order | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    o.id,
                    o.order_number,
                    o.article_summary,
                    os.id AS status_id,
                    os.name AS status_name,
                    pp.id AS pickup_point_id,
                    pp.address AS pickup_address,
                    o.order_date,
                    o.delivery_date,
                    o.customer_name,
                    o.pickup_code
                FROM orders o
                JOIN order_statuses os ON os.id = o.status_id
                JOIN pickup_points pp ON pp.id = o.pickup_point_id
                WHERE o.id = ?
                """,
                (order_id,),
            ).fetchone()
        if row is None:
            return None
        return self._map_order(row)

    def save_order(self, data: dict[str, object], order_id: int | None = None) -> None:
        status_id = self._get_lookup_id('order_statuses', str(data['status_name']))
        pickup_point_id = self._get_lookup_id(
            'pickup_points', str(data['pickup_address']), field='address'
        )
        payload = (
            int(data['order_number']),
            str(data['article_summary']).strip(),
            status_id,
            pickup_point_id,
            str(data['order_date']).strip() if data.get('order_date') else None,
            str(data['delivery_date']).strip() if data.get('delivery_date') else None,
            str(data['customer_name']).strip() if data.get('customer_name') else 'Не указан',
            str(data['pickup_code']).strip() if data.get('pickup_code') else '',
        )
        with self.connect() as connection:
            if order_id is None:
                cursor = connection.execute(
                    """
                    INSERT INTO orders (
                        order_number, article_summary, status_id, pickup_point_id,
                        order_date, delivery_date, customer_name, pickup_code
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    payload,
                )
                new_id = cursor.lastrowid
                self._replace_order_items(connection, new_id, str(data['article_summary']))
            else:
                connection.execute(
                    """
                    UPDATE orders
                    SET order_number = ?,
                        article_summary = ?,
                        status_id = ?,
                        pickup_point_id = ?,
                        order_date = ?,
                        delivery_date = ?,
                        customer_name = ?,
                        pickup_code = ?
                    WHERE id = ?
                    """,
                    (*payload, order_id),
                )
                self._replace_order_items(connection, order_id, str(data['article_summary']))

    def delete_order(self, order_id: int) -> None:
        with self.connect() as connection:
            connection.execute('DELETE FROM orders WHERE id = ?', (order_id,))

    def _replace_order_items(
        self, connection: sqlite3.Connection, order_id: int, article_summary: str
    ) -> None:
        connection.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
        for article, quantity in self.parse_article_summary(article_summary):
            row = connection.execute(
                'SELECT id FROM products WHERE article = ?', (article,)
            ).fetchone()
            if row is not None:
                connection.execute(
                    'INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)',
                    (order_id, row['id'], quantity),
                )

    @staticmethod
    def parse_article_summary(article_summary: str) -> Iterable[tuple[str, int]]:
        parts = [part.strip() for part in article_summary.split(',') if part and part.strip()]
        result: list[tuple[str, int]] = []
        index = 0
        while index + 1 < len(parts):
            article = parts[index]
            try:
                quantity = int(parts[index + 1])
            except ValueError:
                quantity = 1
            result.append((article, quantity))
            index += 2
        return result

    def _get_lookup_id(self, table_name: str, value: str, field: str = 'name') -> int:
        with self.connect() as connection:
            row = connection.execute(
                f'SELECT id FROM {table_name} WHERE {field} = ?',
                (value.strip(),),
            ).fetchone()
        if row is None:
            raise ValueError(f'Значение "{value}" не найдено в таблице {table_name}.')
        return int(row['id'])

    def _get_or_create_lookup_id(self, table_name: str, value: str) -> int:
        value = value.strip()
        with self.connect() as connection:
            row = connection.execute(
                f'SELECT id FROM {table_name} WHERE name = ?',
                (value,),
            ).fetchone()
            if row is not None:
                return int(row['id'])
            cursor = connection.execute(
                f'INSERT INTO {table_name} (name) VALUES (?)',
                (value,),
            )
            return int(cursor.lastrowid)

    @staticmethod
    def _map_product(row: sqlite3.Row) -> Product:
        return Product(
            id=row['id'],
            article=row['article'],
            name=row['name'],
            unit=row['unit'],
            price=float(row['price']),
            supplier_id=row['supplier_id'],
            supplier_name=row['supplier_name'],
            manufacturer_id=row['manufacturer_id'],
            manufacturer_name=row['manufacturer_name'],
            category_id=row['category_id'],
            category_name=row['category_name'],
            discount_percent=int(row['discount_percent']),
            stock_quantity=int(row['stock_quantity']),
            description=row['description'] or '',
            image_path=row['image_path'],
        )

    @staticmethod
    def _map_order(row: sqlite3.Row) -> Order:
        def parse(value: str | None):
            if not value:
                return None
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                return None

        return Order(
            id=row['id'],
            order_number=int(row['order_number']),
            article_summary=row['article_summary'] or '',
            status_id=int(row['status_id']),
            status_name=row['status_name'],
            pickup_point_id=int(row['pickup_point_id']),
            pickup_address=row['pickup_address'],
            order_date=parse(row['order_date']),
            delivery_date=parse(row['delivery_date']),
            customer_name=row['customer_name'] or '',
            pickup_code=row['pickup_code'] or '',
        )
