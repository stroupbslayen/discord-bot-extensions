from orator.migrations import Migration
from orator.schema import Blueprint


class User(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("users") as table:
            table: Blueprint
            table.integer("id")
            table.timestamps()
            table.integer("total_time").default(0)
            table.boolean("checked_in").default(False)

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("users")
