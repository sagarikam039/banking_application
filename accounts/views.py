
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BankAccount, Transaction
import random
from decimal import Decimal
from django.contrib.auth.decorators import login_required

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
