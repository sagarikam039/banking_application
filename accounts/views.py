
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BankAccount, Transaction
import random
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BankAccountSerializer, TransactionSerializer

def home(request):
    return render(request, 'home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        acc_number = random.randint(1000000000, 9999999999)
        BankAccount.objects.create(user=user, account_number=acc_number)
        messages.success(request, 'Account created successfully.')
        return redirect('home')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('home')
# Create your views here.
@login_required
def account_details(request):
    account = BankAccount.objects.get(user=request.user)
    return render(request, 'account_details.html', {'account': account})

@login_required
def deposit_money(request):
    account = BankAccount.objects.get(user=request.user)
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, transaction_type='DEPOSIT', amount=amount)
        return redirect('account')
    return render(request, 'deposit.html')

@login_required
def withdraw_money(request):
    account = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))

        if account.balance >= amount:
            account.balance = account.balance - amount
            account.save()
            Transaction.objects.create(account=account, transaction_type='WITHDRAW', amount=amount)

        return redirect('account')

    return render(request, 'withdraw.html')

@login_required
def transaction_history(request):
    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'transactions.html', {'transactions': transactions})

@login_required
def transfer_money(request):

    sender_account = BankAccount.objects.get(user=request.user)

    if request.method == 'POST':

        receiver_account_number = request.POST.get('receiver_account')

        amount = Decimal(request.POST.get('amount'))

        try:
            receiver_account = BankAccount.objects.get(
                account_number=receiver_account_number
            )

            if sender_account.balance >= amount:

                sender_account.balance -= amount
                receiver_account.balance += amount

                sender_account.save()
                receiver_account.save()

                Transaction.objects.create(
                    account=sender_account,
                    transaction_type='TRANSFER_SENT',
                    amount=amount
                )

                Transaction.objects.create(
                    account=receiver_account,
                    transaction_type='TRANSFER_RECEIVED',
                    amount=amount
                )

                return redirect('account')

        except BankAccount.DoesNotExist:
            pass

    return render(request, 'transfer.html')

@api_view(['GET'])
def account_api(request):

    accounts = BankAccount.objects.all()

    serializer = BankAccountSerializer(accounts, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def deposit_api(request):

    account_number = request.data.get('account_number')
    amount = Decimal(request.data.get('amount'))

    account = BankAccount.objects.get(account_number=account_number)

    account.balance = account.balance + amount
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type='DEPOSIT',
        amount=amount
    )

    return Response({
        'message': 'Amount deposited successfully',
        'account_number': account.account_number,
        'updated_balance': account.balance
    })

@api_view(['POST'])
def withdraw_api(request):

    account_number = request.data.get('account_number')
    amount = Decimal(request.data.get('amount'))

    account = BankAccount.objects.get(account_number=account_number)

    if account.balance >= amount:

        account.balance = account.balance - amount
        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type='WITHDRAW',
            amount=amount
        )

        return Response({
            'message': 'Amount withdrawn successfully',
            'account_number': account.account_number,
            'updated_balance': account.balance
        })

    return Response({
        'message': 'Insufficient balance'
    })

@api_view(['POST'])
def transfer_api(request):

    sender_account_number = request.data.get('sender_account')
    receiver_account_number = request.data.get('receiver_account')
    amount = Decimal(request.data.get('amount'))

    sender_account = BankAccount.objects.get(account_number=sender_account_number)
    receiver_account = BankAccount.objects.get(account_number=receiver_account_number)

    if sender_account.balance >= amount:

        sender_account.balance = sender_account.balance - amount
        receiver_account.balance = receiver_account.balance + amount

        sender_account.save()
        receiver_account.save()

        Transaction.objects.create(
            account=sender_account,
            transaction_type='TRANSFER_SENT',
            amount=amount
        )

        Transaction.objects.create(
            account=receiver_account,
            transaction_type='TRANSFER_RECEIVED',
            amount=amount
        )

        return Response({
            'message': 'Amount transferred successfully',
            'sender_account': sender_account.account_number,
            'receiver_account': receiver_account.account_number,
            'transferred_amount': amount,
            'sender_updated_balance': sender_account.balance
        })

    return Response({
        'message': 'Insufficient balance'
    })