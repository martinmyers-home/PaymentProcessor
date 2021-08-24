import pandas as pd
from pandas import DataFrame

from AccountManagement.account import Account


class AccountManager:
    """
    Container containing all accounts.
    An accounts are requested by client id, if it is not found then a new one is created
    """

    def __init__(self):
        '''

        '''
        self.accounts = {}

    def _create_account(self, account_number: int):
        account = Account(account_number)
        self.accounts[account_number] = account
        return account

    def get_account(self, client: int):
        """
        Returns the account for the given client.  If it does not exist a new one is created and returned
        :param client: id of the client also the unique id of their account
        :return:
        """
        try:
            return self.accounts[client]
        except KeyError:
            return self._create_account(client)

    def accounts_data(self) -> DataFrame:
        """

        :return: A pandas DataFrame containing data on all the accounts with columns
                 "client", "available", "held", "total", "frozen"
                 Rows are ordered by creation time.  Amounts are given to 4 decimal places
        """
        account_data_list = []
        for account in self.accounts.values():
            account_data_list.append(list(account.account_data()))
        return pd.DataFrame(account_data_list, columns=["client", "available", "held", "total", "frozen"])
