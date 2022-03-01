class GoDutchDatabase:
    def __init__(self):
        raise NotImplementedError

    @property
    def users(self):
        # Query the database for the list of usernames.
        raise NotImplementedError

    def append_expense(self, user, expense_name, expense_amount, date):
        raise NotImplementedError

    def append_user(self, user):
        raise NotImplementedError

    def get_monthly_total(self, user, month):
        raise NotImplementedError

