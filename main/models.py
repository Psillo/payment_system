from django.db import models
from django.contrib.auth.models import User


class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='bank_accounts')
    balance = models.DecimalField(max_digits=10, decimal_places=2,
                                  default=0)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValueError
        super().save(*args, **kwargs)


class Transfer(models.Model):
    user_of = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='completed_transfers')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='accepted_transfers')
    of = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                           related_name='transfers_of')
    to = models.ForeignKey(BankAccount, on_delete=models.CASCADE,
                           related_name='transfers_to')
    amount = models.DecimalField(max_digits=10, decimal_places=2,
                                 default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.amount < 1:
            raise ValueError
        super().save(*args, **kwargs)
