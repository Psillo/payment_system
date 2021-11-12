from django.contrib import admin

from .models import BankAccount, Transfer


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'balance']


@admin.register(Transfer)
class CompletedTransferAdmin(admin.ModelAdmin):
    list_display = ['user_of', 'user_to', 'of',
                    'to', 'amount', 'date']
