import random
import string
from datetime import datetime


def generate_id(random_str: tuple, length: int) -> str:
    return "".join(random_str)[:length]


def weekday(dt: datetime) -> str:
    return f"{dt:%A}"


def main() -> None:
    today = datetime.today()
    print(f"Today is a {weekday(today)}")
    ln = 10
    x = tuple(random.choice(string.ascii_uppercase + string.digits) for _ in range(ln))
    print(f"Your id = {generate_id(x, 5)}")


if __name__ == "__main__":
    main()
