from decimal import Decimal

from AccountManagement.account import Account, InsufficientFunds, AccountLocked


class InvalidTransactionType(Exception):
    pass


DEPOSIT = "deposit"
WITHDRAWAL = "withdrawal"
DISPUTE = "dispute"
RESOLVE = "resolve"
CHARGEBACK = "chargeback"

IMPLEMENTED = [DEPOSIT, WITHDRAWAL, DISPUTE, RESOLVE, CHARGEBACK]
DISPUTABLE = [DEPOSIT]
WITH_AMOUNT = [DEPOSIT, WITHDRAWAL]


class Transaction:
    """
    Transient class representing a transaction.   Hass attributes type, tx (id) and amount, but not the account it
    applies to.  This is supplied as a parameter in the apply_to method.
    """

    def __init__(self, tx_type: str, tx: int, amount: float = 0.0):
        """
        Creates a transaction with the given attributes.  Will raise an appropriate exception if the types are incorrect
        :param tx_type: determines what the transaction will do when applied to anaccount.
                        Must be in the IMPLEMENTED lis
        :param tx: id of the transaction (is labelled tx in the transaction csv)
        :param amount: the amount of the  transaction.  Only given for certain types.
        """
        if tx_type.lower() in IMPLEMENTED:
            self.type = tx_type.lower()
        else:
            raise InvalidTransactionType
        self.tx = int(tx)
        self.amount = Decimal(amount)

    def apply_to(self, account: Account):
        """
        Applies itself to the account given by calling the appropriate method depending on the transaction type.
        If the transaction is disputable will be saved with  the account provided the transaction was executed

        :param account: account the transaction is to be applied to
        """
        try:
            if self.type == DEPOSIT:
                account.deposit(self.amount)
            elif self.type == WITHDRAWAL:
                account.withdrawal(self.amount)
            elif self.type == DISPUTE:
                account.dispute(self.tx)
            elif self.type == RESOLVE:
                account.resolve(self.tx)
            elif self.type == CHARGEBACK:
                account.chargeback(self.tx)
            else:
                raise InvalidTransactionType
            if self.type in DISPUTABLE:
                account.store_transaction(self)
        except (InvalidTransactionType, InsufficientFunds, AccountLocked):
            pass
