from orator.migrations import Migration


class Banks(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("currency_banks") as table:
            table: Blueprint
            table.big_integer("id")
            table.primary("id")
            table.timestamps()
            table.text("currency").default("dollars")
            table.json("approved_roles").default("[]")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("currency_banks")
