from orator.migrations import Migration


class Accounts(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("currency_accounts") as table:
            table: Blueprint
            table.big_integer("id")
            table.primary("id")
            table.timestamps()
            table.big_integer("guild").unsigned()
            table.foreign("guild").references("id").on("currency_banks")
            table.big_integer("balance").default(0)

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("currency_accounts")
