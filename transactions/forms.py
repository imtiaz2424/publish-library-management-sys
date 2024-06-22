from django import forms
from .models import Transaction
from transactions.constants import BORROW
from posts.models import Post, Order
from django.contrib import messages
from django.shortcuts import redirect

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.users = kwargs.pop('users') 
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True 
        self.fields['transaction_type'].widget = forms.HiddenInput() 

    def save(self, commit=True):
        self.instance.users = self.users
        self.instance.balance_after_transaction = self.users.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): 
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} ৳'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        users = self.users
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = users.balance 
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} ৳'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} ৳'
            )

        if amount > balance: 
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount
    



class BorrowForm(TransactionForm):

    def clean_amount(self):
        users = self.users
        min_borrow_amount = 0
        max_borrow_amount = 50000
        balance = users.balance 
        amount = self.cleaned_data.get('amount')
        if amount < min_borrow_amount:
            raise forms.ValidationError(
                f'You can borrow at least {min_borrow_amount} ৳'
            )
        if amount > max_borrow_amount:
            raise forms.ValidationError(
                f'You can borrow at most {max_borrow_amount} ৳'
            )

        if amount > balance: 
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not borrow more than your account balance'
            )

        return amount

       
    