"""Banks Model."""
import json
from discord import Member, Role
from orator.orm import has_many

from bot.database import Model


class Banks(Model):
    """Banks Model."""

    id: int
    guild: int
    currency: int
    approved_roles: str

    __table__ = "currency_banks"
    __fillable__ = ["id"]

    @has_many(foreign_key="guild")
    def accounts(self):
        from . import Accounts

        return Accounts

    def get_account(self, member: Member):
        from . import Accounts

        account = self.accounts.filter(lambda user: user.id == member.id)
        if not account.first():
            account = Accounts(id=member.id, guild=member.guild.id, balance=0)
            account.save()
            return account
        return account.first()

    def add_roles(self, *roles: [Role]):
        is_string = isinstance(self.approved_roles, str)
        js = self.approved_roles
        if is_string:
            js = json.loads(self.approved_roles)
        for role in roles:
            if role.id not in js:
                js.append(role.id)
        if is_string:
            self.approved_roles = json.dumps(js)
        else:
            self.approved_roles = js
        self.save()

    def remove_roles(self, *roles: [Role]):
        is_string = isinstance(self.approved_roles, str)
        js = self.approved_roles
        if is_string:
            js = json.loads(self.approved_roles)
        for role in roles:
            try:
                js.pop(js.index(role.id))
            except:
                pass
        if is_string:
            self.approved_roles = json.dumps(js)
        else:
            self.approved_roles = js
        self.save()

    @property
    def approved(self):
        js = self.approved_roles
        if isinstance(self.approved_roles, str):
            js = json.loads(self.approved_roles)
        return js

    def __repr__(self):
        return f"Bank: {self.id}"

    def __eq__(self, other):

        return self.id == other.id
