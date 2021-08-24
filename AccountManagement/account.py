from decimal import Decimal


class InsufficientFunds(Exception):
    pass


class AccountLocked(Exception):
    pass


class Account:
    """
    Class representing a bank account.  Various operations can be performed on it.  Transactions which could be disputed
    later are stored.  Any transactions under dispute are stored.  Once a dispute has been resolved (or chargedback) the
    transaction is no longer stored (cannot be subsequently disputed)
    """

    def __init__(self, client: int):
        """
        Creates an account with the client as its own id.  Account has no assets and is not locked
        :param client: id of the client also used as id of the account (client can only have one account)
        """
        self.client = int(client)
        self.available = Decimal(0.0)
        self.held = Decimal(0.0)
        self.locked = False
        self.undisputed_transactions = {}
        self.disputed_transactions = {}

    def total(self) -> Decimal:
        """

        :return: total amount in account regardless of held or available
        """
        return self.available + self.held

    def deposit(self, amount: Decimal):
        """
        Increase the amount of available funds by the given amount

        :param amount: amount deposited
        """
        if not self.locked:
            self.available += Decimal(amount)
        else:
            raise AccountLocked

    def withdrawal(self, amount: Decimal):
        """
        Reduce the amount of available funds by the given amount

        :param amount: amount withdrawn
        """
        if not self.locked:
            if Decimal(amount) > self.available:
                raise InsufficientFunds
            else:
                self.available -= amount
        else:
            raise AccountLocked

    def store_transaction(self, transaction):
        """
        Stores the id and amount of the transaction for future reference in case it is later disputed.
        It is up to the caller to check that the transaction type is disputable.

        :param transaction: The transaction whose id and amount are to be stored
        :return:
        """
        self.undisputed_transactions[transaction.tx] = transaction.amount

    def dispute(self, tx: int):
        """
        Sets a transaction into a disputed state.  The amount of the transaction is held, that is moved from the
        available area to the held area of the account.  Note may leave available funds to be less than zero.
        If transaction was not a disputable transaction i.e. a deposit (for this client) then it is ignored and account
        remains unchanged.

        :param tx: id of disputed transaction
        """
        if not self.locked:
            if tx in self.undisputed_transactions:
                disputed_amount = self.undisputed_transactions[tx]
                self.available -= disputed_amount
                self.held += disputed_amount
                self.disputed_transactions[tx] = disputed_amount
                self.undisputed_transactions.pop(tx)
        else:
            raise AccountLocked

    def resolve(self, tx: int):
        """
        Implements a dispute resolution - amount from transaction id given is released from held area of account back
        into the avialable area.
        If transaction is not already in dispute (for this client) then it is ignored and account remains unchanged.

        :param tx: id of transaction to be resolved
        """
        if not self.locked:
            if tx in self.disputed_transactions:
                disputed_amount = self.disputed_transactions[tx]
                self.available += disputed_amount
                self.held -= disputed_amount
                self.disputed_transactions.pop(tx)
                # assume can't be disputed again so not put back in undisputed_transactions dict
        else:
            raise AccountLocked

    def chargeback(self, tx: int):
        """
        Implements a chargeback - amount from transaction id given is taken from held area of account.  The account is then frozen and no further transactions will be processed on it.
        If transaction is not already in dispute (for this client) then it is ignored and account remains unchanged.

        :param tx: id of transaction to be charged back.
        """
        if not self.locked:
            if tx in self.disputed_transactions:
                disputed_amount = self.disputed_transactions[tx]
                self.held -= disputed_amount
                self.disputed_transactions.pop(tx)
                self.locked = True
        else:
            raise AccountLocked

    def account_data(self):
        """
        returns data as a tuple [client, available, held, total, locked].  Amounts given to 4 decimal places
        """
        return self.client, round(self.available, 4), round(self.held, 4), round(self.total(), 4), self.locked
