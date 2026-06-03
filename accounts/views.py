
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

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
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        acc_number = str(random.randint(1000000000, 9999999999))

        while BankAccount.objects.filter(account_number=acc_number).exists():
            acc_number = str(random.randint(1000000000, 9999999999))

        BankAccount.objects.create(
            user=user,
            account_number=acc_number
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_api(request):
    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    data = []

    for transaction in transactions:
        data.append({
            "id": transaction.id,
            "transaction_type": transaction.transaction_type,
            "amount": transaction.amount,
            "created_at": transaction.created_at,
        })

    return Response(data)
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
@permission_classes([IsAuthenticated])
def account_api(request):

    account = BankAccount.objects.get(user=request.user)

    return Response({
        "username": request.user.username,
        "account_number": account.account_number,
        "balance": account.balance
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def risk_analyzer_api(request):

    account = BankAccount.objects.get(user=request.user)

    transactions = Transaction.objects.filter(account=account)

    total_transactions = transactions.count()

    total_withdrawals = transactions.filter(transaction_type='WITHDRAW').count()

    total_transfers = transactions.filter(transaction_type='TRANSFER_SENT').count()

    balance = account.balance

    risk_level = "Low Risk"

    reason = "Your account activity looks normal."

    if balance < 500 or total_withdrawals > 5 or total_transfers > 5:
        risk_level = "High Risk"
        reason = "Your balance is low or there are many outgoing transactions."

    elif balance < 2000 or total_withdrawals > 2 or total_transfers > 2:
        risk_level = "Medium Risk"
        reason = "Your account has moderate outgoing activity."

    return Response({
        "username": request.user.username,
        "balance": balance,
        "total_transactions": total_transactions,
        "total_withdrawals": total_withdrawals,
        "total_transfers": total_transfers,
        "risk_level": risk_level,
        "reason": reason
    })

@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')

    if password1 != password2:
        return Response({"message": "Passwords do not match"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1
    )

    acc_number = str(random.randint(1000000000, 9999999999))

    while BankAccount.objects.filter(account_number=acc_number).exists():
        acc_number = str(random.randint(1000000000, 9999999999))

    BankAccount.objects.create(
        user=user,
        account_number=acc_number
    )

    return Response({"message": "Account created successfully"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    account = BankAccount.objects.get(user=request.user)

    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "account_number": account.account_number,
        "balance": str(account.balance),
        "created_at": account.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    })