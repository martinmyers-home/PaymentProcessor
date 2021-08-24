import decimal

import pandas as pd

from TransactionEngine.transaction import WITH_AMOUNT, Transaction, InvalidTransactionType


class TransactionList:
    """
    List of transaction as a pandas Dataframe with method to process itself
    """

    def __init__(self, transactions: pd.DataFrame):
        """
        Stores the given transactions as an attribute
        :param transactions: transactions as pandas Dataframe
        """
        self.transactions = transactions

    def process(self, account_manager):
        """
        For each element in the list creates a Transaction instance.  If that was valid applies it to the account in the
        transaction which it gets from the account manager.
        :param account_manager:
        :return:
        """
        for index, transaction_row in self.transactions.iterrows():
            try:
                transaction_type = transaction_row.loc['type'].lower()
                if transaction_type in WITH_AMOUNT:
                    transaction = Transaction(tx_type=transaction_type,
                                              tx=transaction_row.loc['tx'],
                                              amount=transaction_row.loc['amount'])
                else:
                    transaction = Transaction(tx_type=transaction_type,
                                              tx=transaction_row.loc['tx'])
                account = account_manager.get_account(transaction_row.loc['client'])
                transaction.apply_to(account)
            except (InvalidTransactionType, decimal.InvalidOperation, ValueError):
                pass
