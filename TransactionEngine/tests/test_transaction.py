import decimal
import unittest
from unittest.mock import Mock, call

from TransactionEngine.transaction import Transaction, DEPOSIT, WITHDRAWAL, DISPUTE, RESOLVE, CHARGEBACK, \
    InvalidTransactionType


class TestTransaction(unittest.TestCase):

    def test_tx_types(self):
        transaction = Transaction(tx_type="deposit", tx=1, amount=1.0)
        self.assertEqual(transaction.type, DEPOSIT)
        transaction = Transaction(tx_type="withdrawal", tx=1, amount=1.0)
        self.assertEqual(transaction.type, WITHDRAWAL)
        transaction = Transaction(tx_type="dispute", tx=1)
        self.assertEqual(transaction.type, DISPUTE)
        transaction = Transaction(tx_type="resolve", tx=1)
        self.assertEqual(transaction.type, RESOLVE)
        transaction = Transaction(tx_type="chargeback", tx=1)
        self.assertEqual(transaction.type, CHARGEBACK)
        self.assertRaises(InvalidTransactionType, Transaction, "mytxtype", 1)

    def test_tx_types_case_insensitive(self):
        transaction = Transaction(tx_type="DEPOSIT", tx=1, amount=1.0)
        self.assertEqual(transaction.type, DEPOSIT)
        transaction = Transaction(tx_type="Withdrawal", tx=1, amount=1.0)
        self.assertEqual(transaction.type, WITHDRAWAL)
        transaction = Transaction(tx_type="disPute", tx=1)
        self.assertEqual(transaction.type, DISPUTE)
        transaction = Transaction(tx_type="RESOLVE", tx=1)
        self.assertEqual(transaction.type, RESOLVE)
        transaction = Transaction(tx_type="ChargeBack", tx=1)
        self.assertEqual(transaction.type, CHARGEBACK)

    def test_invalid_id_and_amount(self):
        transaction = Transaction(tx_type="deposit", tx=1, amount='1.0')
        self.assertEqual(transaction.type, DEPOSIT)
        self.assertRaises(decimal.InvalidOperation, Transaction, "deposit", 1, 'I')
        transaction = Transaction(tx_type="dispute", tx='1')
        self.assertEqual(transaction.type, DISPUTE)
        self.assertRaises(ValueError, Transaction, "resolve", 'x')

    def test_routing_apply_to(self):
        transaction = Transaction(tx_type="deposit", tx=1, amount=3.0)
        account = Mock()
        transaction.apply_to(account)
        self.assertEqual(account.mock_calls[0], call.deposit(decimal.Decimal('3')))
        transaction = Transaction(tx_type="withdrawal", tx=1, amount=2.0)
        account2 = Mock()
        transaction.apply_to(account2)
        self.assertEqual(account2.mock_calls, [call.withdrawal(decimal.Decimal('2'))])
        transaction = Transaction(tx_type="dispute", tx=1)
        account3 = Mock()
        transaction.apply_to(account3)
        self.assertEqual(account3.mock_calls, [call.dispute(1)])
        transaction = Transaction(tx_type="resolve", tx=1)
        account4 = Mock()
        transaction.apply_to(account4)
        self.assertEqual(account4.mock_calls, [call.resolve(1)])
        transaction = Transaction(tx_type="chargeback", tx=1)
        account5 = Mock()
        transaction.apply_to(account5)
        self.assertEqual(account5.mock_calls, [call.chargeback(1)])


if __name__ == '__main__':
    unittest.main()
