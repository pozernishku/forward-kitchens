"""https://www.arjancodes.com/products/the-software-designer-mindset/categories/2150535932/posts/2158614542"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AA:
    _length: int = 0


class A:
    def __init__(self) -> None:
        self._length = 0


class B:
    def __init__(self, x: int, y: str = "hello", l: list[int] | None = None) -> None:
        self.x = x
        self.y = y
        self.l = [] if not l else l


def default_list():
    return []


@dataclass
class BB:
    x: int
    y: str = "hello"
    l: list[int] | None = field(default_factory=default_list)  # or just use list


class C:
    def __init__(self, a: int = 3) -> None:
        self.a = a
        self.b = a + 3


@dataclass  # @dataclass(frozen=True)
class CC:
    a: int = 3
    b: int = field(init=False)

    def __post_init__(self):
        self.b = self.a + 3


@dataclass
class Customer:
    name: str
    address: str
    email: str


@dataclass
class Phone:
    brand: str
    model: str
    price: int
    serial_number: str


@dataclass
class Plan:
    customer: Customer
    phone: Phone
    start_date: datetime
    number_of_months: int
    monthly_price: int
    phone_included: bool


if __name__ == "__main__":
    c = C(5)
    print(c, c.a, c.b)
    cc = CC(5)
    print(cc)
