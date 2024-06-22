from django.contrib import admin

# from transactions.models import Transaction
from .models import Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['users', 'amount', 'balance_after_transaction', 'transaction_type']
    
    def save_model(self, request, obj, form, change):
        obj.users.balance += obj.amount
        obj.balance_after_transaction = obj.users.balance
        obj.users.save()
        super().save_model(request, obj, form, change)

