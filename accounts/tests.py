
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import BankAccount, Transaction


class UserModelTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass123'
        )

        self.assertEqual(user.username, 'testuser')


class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='sagarika',
            password='test123'
        )

    def test_login(self):

        response = self.client.login(
            username='sagarika',
            password='test123'
        )

        self.assertTrue(response)

class DepositTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='deposituser',
            password='test123'
        )

        self.account = BankAccount.objects.create(
            user=self.user,
            account_number='1234567890',
            balance=Decimal('0.00')
        )

    def test_deposit_amount(self):
        amount = Decimal('500.00')

        self.account.balance = self.account.balance + amount
        self.account.save()

        Transaction.objects.create(
            account=self.account,
            transaction_type='DEPOSIT',
            amount=amount
        )

        self.account.refresh_from_db()

        self.assertEqual(self.account.balance, Decimal('500.00'))
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().transaction_type, 'DEPOSIT')

class WithdrawTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='withdrawuser',
            password='test123'
        )

        self.account = BankAccount.objects.create(
            user=self.user,
            account_number='9876543210',
            balance=Decimal('1000.00')
        )

    def test_withdraw_amount(self):
        amount = Decimal('300.00')

        if self.account.balance >= amount:
            self.account.balance = self.account.balance - amount
            self.account.save()

            Transaction.objects.create(
                account=self.account,
                transaction_type='WITHDRAW',
                amount=amount
            )

        self.account.refresh_from_db()

        self.assertEqual(self.account.balance, Decimal('700.00'))
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().transaction_type, 'WITHDRAW')

class TransferTest(TestCase):

    def setUp(self):
        self.sender_user = User.objects.create_user(
            username='senderuser',
            password='test123'
        )

        self.receiver_user = User.objects.create_user(
            username='receiveruser',
            password='test123'
        )

        self.sender_account = BankAccount.objects.create(
            user=self.sender_user,
            account_number='1111111111',
            balance=Decimal('1000.00')
        )

        self.receiver_account = BankAccount.objects.create(
            user=self.receiver_user,
            account_number='2222222222',
            balance=Decimal('200.00')
        )

    def test_transfer_amount(self):
        amount = Decimal('300.00')

        if self.sender_account.balance >= amount:
            self.sender_account.balance = self.sender_account.balance - amount
            self.receiver_account.balance = self.receiver_account.balance + amount

            self.sender_account.save()
            self.receiver_account.save()

            Transaction.objects.create(
                account=self.sender_account,
                transaction_type='TRANSFER_SENT',
                amount=amount
            )

            Transaction.objects.create(
                account=self.receiver_account,
                transaction_type='TRANSFER_RECEIVED',
                amount=amount
            )

        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()

        self.assertEqual(self.sender_account.balance, Decimal('700.00'))
        self.assertEqual(self.receiver_account.balance, Decimal('500.00'))
        self.assertEqual(Transaction.objects.count(), 2)
# Create your tests here.
