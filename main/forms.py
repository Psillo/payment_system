from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BankAccountForm(forms.Form):
    balance = forms.DecimalField(min_value=0.00)


class TransferForm(forms.Form):
    of = forms.CharField(
        max_length=255, min_length=1,
        help_text='Введите номер своего счета. ' +
                  'Или номера, через запятую: 1,2,3'
    )
    to = forms.IntegerField(
        min_value=1,
        help_text='Введите номер счета, ' +
                  'на который хотите перевести деньги.'
    )
    amount = forms.DecimalField(min_value=0.01,
                                help_text='Введите сумму перевода.')
