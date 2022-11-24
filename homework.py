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
                if get_day_a_week_ago() < record.date <= dt.now().date()
            )
        )


class CaloriesCalculator(Calculator):
    """Calorie calculator."""

    def get_calories_remained(self) -> str:
        """Calculates the calorie remained for today."""
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            return (
                "Сегодня можно съесть что-нибудь ещё, "
                f"но с общей калорийностью не более {remainder:.0f} кКал"
            )
        return "Хватит есть!"


class CashCalculator(Calculator):
    """Money calculator."""

    USD_RATE = 60.5043
    EURO_RATE = 62.2850

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Returns a message about the status of
        the daily balance in the currency.

        :param currency: currency - "usd"/"eur"/"rub"
        :return: None
        """
        сurrency_signs = {
            "usd": (self.USD_RATE, "USD"),
            "eur": (self.EURO_RATE, "Euro"),
            "rub": (1.0, "руб"),
        }
        currency_contraction = сurrency_signs[currency][1]
        remainder = float(self.limit - self.get_today_stats())
        if remainder == 0:
            return "Денег нет, держись"
        ballanse = round(abs(remainder / сurrency_signs[currency][0]), 2)
        if remainder > 0:
            return f"На сегодня осталось {ballanse} {currency_contraction}"
        return f"Денег нет, держись: твой долг - {ballanse} {currency_contraction}"


class Record:
    """A class describing a single entry."""

    def __init__(self, amount: int, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.now().date()
        else:
            self.date = dt.strptime(date, "%d.%m.%Y").date()


if __name__ == "__main__":
    cash_calculator = CashCalculator(545)
    cash_calculator.add_record(Record(amount=1, comment="Кофе"))
    cash_calculator.add_record(Record(amount=2, comment="Булочка"))
    print(cash_calculator.get_today_cash_remained("rub"))
