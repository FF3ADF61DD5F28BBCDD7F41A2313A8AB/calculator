"""
    Money and calories calculator.
"""
import datetime
from datetime import datetime as dt


class Calculator:
    """Parent class."""

    def __init__(self, limit: int) -> None:
        self.limit = float(limit)
        self.records = []

    def add_record(self, record: "Record") -> None:
        """Saves a record for accounting."""
        self.records.append(record)

    def get_today_stats(self) -> float:
        """Count how much money you spent today."""
        return sum(
            (record.amount for record in self.records if record.date == dt.now().date())
        )

    def get_week_stats(self) -> float:
        """Calculates how much was spent in the last 7 days."""

        def get_day_a_week_ago():
            return dt.today().date() - datetime.timedelta(days=7)

        return sum(
            (
                record.amount
                for record in self.records
                if record.date >= get_day_a_week_ago()
            )
        )


class CaloriesCalculator(Calculator):
    """Calorie calculator."""

    def get_calories_remained(self) -> None:
        """Calculates the calorie remained for today."""
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            print(
                "Сегодня можно съесть что-нибудь ещё, "
                f"но с общей калорийностью не более {remainder:.0f} кКал"
            )
        else:
            print("Хватит есть!")


class CashCalculator(Calculator):
    """Money calculator."""

    USD_RATE = 60.5043
    EUR_RATE = 62.2850

    сurrency_signs = {
        "usd": (USD_RATE, "USD"),
        "eur": (EUR_RATE, "Euro"),
        "rub": (1.0, "руб"),
    }

    def get_today_cash_remained(self, currency: str) -> None:
        """
        Returns a message about the status of
        the daily balance in the currency.

        :param currency: currency - "usd"/"eur"/"rub"
        :return: None
        """
        currency_contraction = self.сurrency_signs[currency][1]
        remainder = float(
            ((self.limit - self.get_today_stats()) * self.сurrency_signs[currency][0])
        )
        if remainder == 0:
            print("Денег нет, держись")
        elif remainder > 0:
            print(f"На сегодня осталось {remainder:.2f} {currency_contraction}")
        elif remainder < 0:
            print(
                f"Денег нет, держись: твой долг - {remainder:.2f} {currency_contraction}"
            )


class Record:
    """A class describing a single entry."""

    def __init__(self, amount: int, comment: str, date=dt.now()):
        self.amount = amount
        self.comment = comment
        if date == dt.now():
            self.date = date.date()
        else:
            self.date = dt.strptime(date, "%d.%m.%Y").date()


if __name__ == "__main__":
    cash_calculator = CaloriesCalculator(545)
    cash_calculator.add_record(Record(amount=145, comment="Кофе"))
    cash_calculator.add_record(Record(amount=300, comment="Булочка"))
    cash_calculator.get_calories_remained()
