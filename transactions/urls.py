from django.urls import path
from .views import DepositMoneyView, WithdrawMoneyView, TransactionReportView, BorrowView, BorrowingHistoryView
from . import views


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),   
    path("borrow/", BorrowView.as_view(), name="borrow_book"),   
    path("borrow_report/", BorrowingHistoryView.as_view(), name="borrowing_history"), 
    path("buy_now/<int:id>/", views.buy_now, name="buy_now"),
    path("returnbook/<int:id>/", views.return_book, name="return_book"), 
]