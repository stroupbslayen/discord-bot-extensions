"""Accounts Model."""
from orator.orm import belongs_to
from bot.database import Model


class Accounts(Model):
    """Accounts Model."""

    id: int
    guild: int  # foreign key
    balance: int
    __table__ = "currency_accounts"
    __fillable__ = ["id", "balance", "guild"]

    @belongs_to(foreign_key="guild")
    def bank(self):
        from . import Banks

        return Banks

    def __repr__(self):
        return f"Account: {self.id}"

    def __eq__(self, other):
        print(self.id, other.id)
        return self.id == other.id
