"""User Model."""

from discord import Member

from bot.database import Model


class User(Model):
    """User Model."""

    __table__ = "users"
    __fillable__ = ["id"]

    @classmethod
    def get(cls, member: Member):
        user = cls.find_or_new(member.id)
        if not hasattr(user, "checked_in"):
            user.id = member.id
            user.save()
            user = cls.find(member.id)
        return user
