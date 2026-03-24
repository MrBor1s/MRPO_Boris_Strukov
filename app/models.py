from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(slots=True)
class User:
    id: int
    full_name: str
    login: str
    password: str
    role: str


@dataclass(slots=True)
class Product:
    id: int
    article: str
    name: str
    unit: str
    price: float
    supplier_id: int
    supplier_name: str
    manufacturer_id: int
    manufacturer_name: str
    category_id: int
    category_name: str
    discount_percent: int
    stock_quantity: int
    description: str
    image_path: Optional[str]

    @property
    def discounted_price(self) -> float:
        return round(self.price * (1 - self.discount_percent / 100), 2)


@dataclass(slots=True)
class Order:
    id: int
    order_number: int
    article_summary: str
    status_id: int
    status_name: str
    pickup_point_id: int
    pickup_address: str
    order_date: Optional[date]
    delivery_date: Optional[date]
    customer_name: str
    pickup_code: str
