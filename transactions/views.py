from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from posts.models import Post, Order
from user.models import UserAccount
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView
from transactions.constants import DEPOSIT, WITHDRAWAL, BORROW
from datetime import datetime
from django.db.models import Sum
from transactions.forms import (
    DepositForm,
    WithdrawForm,
    BorrowForm,   
)
from transactions.models import Transaction
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'users': self.request.user.users
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        users = self.request.user.users        
        users.balance += amount
        users.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "transactions/deposite_email.html")
        
        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.users.balance -= form.cleaned_data.get('amount')   
        self.request.user.users.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}৳ from your account'
        )
        send_transaction_email(self.request.user, amount, "Withdrawal Message", "transactions/withdrawal_email.html")
        return super().form_valid(form)





class BorrowView(TransactionCreateMixin, LoginRequiredMixin):
    form_class = BorrowForm
    title = 'Borrow Book'

    def get_initial(self):
        initial = {'transaction_type': BORROW}
        return initial    
    
    def save(self, commit=True):
        self.instance.transaction_type = BORROW
        self.instance.timestamp = timezone.now() 
        return super().save(commit=commit)

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        user_profile = self.request.user.users

        user_profile.balance -= amount
        user_profile.save(update_fields=['balance'])

        transaction = form.save(commit=False)
        transaction.amount = amount
        transaction.save()

        send_transaction_email(
            self.request.user,
            amount,
            "Book Borrowing Confirmation",
            "transactions/borrowing_email.html"
        )        

        messages.success(
            self.request,
            f'Successfully borrowed {"{:,.2f}".format(float(amount))}৳. Check your email for confirmation.'
        )
        
        return super().form_valid(form)




    
class TransactionReportView(LoginRequiredMixin, ListView):
    
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            users = self.request.user.users
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.users.balance
       
        return queryset.distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'users': self.request.user.users
        })

        return context
    


class BorrowingHistoryView(LoginRequiredMixin, ListView):
    template_name = 'transactions/borrowing_history.html'
    model = Transaction
    balance = 0 

    def get_queryset(self):
        return Transaction.objects.filter(
            users=self.request.user.users,
            transaction_type=BORROW
        ).order_by('-timestamp')




@login_required  
def buy_now(request, id):
    post = Post.objects.get(pk=id)
    user = request.user.users
    if post.quantity > 0 and user.balance >= post.book_price:        
        post.quantity -= 1
        post.save()
        user.balance -= post.book_price
        user.save()
        order = Order(user=request.user, post=post)
        order.save()

        balance_after_transaction = user.balance

        transaction = Transaction(
            users=user,
            amount=post.book_price,
            transaction_type=3,
            timestamp=timezone.now(),
            balance_after_transaction=balance_after_transaction
        )
        transaction.save()
       
        messages.success(request, 'Book borrowed Successfully')
        send_transaction_email(
            request.user, post.book_price,
            "Book Borrowd Confirmation",
            "transactions/borrowing_email.html"
        )
        return redirect('transaction_report')
    else:
        messages.warning(request, 'Purchase failed: Not enough stock or insufficient balance')
        return redirect('transaction_report') 
    


    
@login_required
def return_book(request, id):
    post = Post.objects.get(pk=id)
    user = request.user.users
    order = request.user.users
    
    if post.quantity >= 0 and user.balance >= post.book_price:        
        post.quantity += 1
        post.save()
        user.balance += post.book_price
        user.save()
        order.active = False
        order.save()

        balance_after_transaction = user.balance

        transaction = Transaction(
            users=user,
            amount=post.book_price,
            transaction_type=4,
            timestamp=timezone.now(),
            balance_after_transaction=balance_after_transaction
        )
        transaction.save()

    messages.success(request, 'Book returned successfully. Amount credited to your account.')
    send_transaction_email(
        request.user, post.book_price,
        "Book Return Confirmation",
        "transactions/return_confirmation_email.html" 
    )
    return redirect('transaction_report')