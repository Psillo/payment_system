import decimal

from django.db import transaction
from payment_system.celery import app

from .models import BankAccount, User, Transfer


@app.task(bind=True)
def trasfer_send(self, of, to, amount, user_id):
    amount = decimal.Decimal(amount)
    to = int(to)

    try:
        ofs = of.split(',')
    except:
        ofs = [int(of)]

    ofs = [int(of) for of in ofs]
    of_amount = amount / len(ofs)

    with transaction.atomic():
        user = User.objects.get(id=int(user_id))
        to_bank_account = BankAccount.objects.get(
            id=to
        )

        for of in ofs:
            bank_account = BankAccount.objects.get(id=of, user=user)
            bank_account.balance = bank_account.balance - of_amount
            bank_account.save()
            Transfer.objects.create(
                user_of=user,
                user_to=to_bank_account.user,
                of=bank_account,
                to=to_bank_account,
                amount=of_amount
            )
        to_bank_account.balance = to_bank_account.balance + amount
        to_bank_account.save()
