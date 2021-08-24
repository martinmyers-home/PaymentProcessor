import sys
import pandas as pd

from AccountManagement.account_manager import AccountManager
from TransactionEngine.transaction_list import TransactionList


def payment_engine(transaction_filename: str):
    """
    Applies the set of transactions in the given csv file.  Outputs the resulting account details to standard output in
    csv format i.e. when calling need to divert output to a csv file

    :param transaction_filename: filename containing transactions
    """
    try:
        transaction_list = TransactionList(pd.read_csv(transaction_filename))
        account_manager = AccountManager()
        transaction_list.process(account_manager)
        accounts = account_manager.accounts_data()
        print(accounts.to_csv(index=False))
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    payment_engine(sys.argv[1])
