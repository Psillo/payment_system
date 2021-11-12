from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)

from .models import BankAccount, User
from .forms import BankAccountForm, TransferForm
from .tasks import trasfer_send


@login_required
def create_bank_account(request):
    if request.method == 'POST':
        bank_account_form = BankAccountForm(request.POST)

        if bank_account_form.is_valid():
            user = User.objects.get(username=request.user)
            BankAccount.objects.create(
                user=user,
                balance=bank_account_form.cleaned_data['balance']
            )

            return redirect('bank_accounts')
    else:
        bank_account_form = BankAccountForm()
    return render(request,
                  'pages/create_bank_account.html',
                  {'section': 'bank_accounts',
                   'bank_account_form': bank_account_form})


@login_required
def bank_accounts(request):
    user = request.user
    bank_accounts = BankAccount.objects.filter(
        user=user
    )
    return render(request,
                  'pages/bank_accounts.html',
                  {'section': 'bank_accounts',
                   'bank_accounts': bank_accounts})


@login_required
def bank_account_info(request, id):
    bank_account = BankAccount.objects.get(id=id)
    len_completed_transfers = len(
        list(
            bank_account.transfers_of.all()
        )
    )
    len_accepted_transfers = len(
        list(
            bank_account.transfers_to.all()
        )
    )
    return render(request,
                  'pages/bank_account_info.html',
                  {'section': 'bank_accounts',
                   'bank_account': bank_account,
                   'len_completed_transfers': len_completed_transfers,
                   'len_accepted_transfers': len_accepted_transfers})


@login_required
def transfers(request):
    if request.method == 'POST':
        transfer_form = TransferForm(request.POST)

        if transfer_form.is_valid():
            of = transfer_form.cleaned_data['of']
            to = transfer_form.cleaned_data['to']
            amount = transfer_form.cleaned_data['amount']
            trasfer_send.delay(of, to,
                               amount, request.user.id)

            return redirect('statistics_of_incoming_transfers')
    else:
        transfer_form = TransferForm()
    return render(request,
                  'pages/transfers.html',
                  {'section': 'transfers',
                   'transfer_form': transfer_form})


@login_required
def statistics_of_incoming_transfers(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    order_by = request.GET.get(
        'order_by'
    ) if request.GET.get('order_by') else 'id'

    try:
        incoming_transfers = list(
            request.user.completed_transfers.filter(
                id__contains=search
            ).order_by(order+order_by)
        )
    except:
        incoming_transfers = list(
            request.user.completed_transfers.all()
        )

    incoming_transfers_paginator = Paginator(incoming_transfers, 10)
    page = request.GET.get('page')

    try:
        page_incoming_transfers = incoming_transfers_paginator.page(
            page
        )
    except PageNotAnInteger:
        page_incoming_transfers = incoming_transfers_paginator.page(
            1
        )
    except EmptyPage:
        page_incoming_transfers = incoming_transfers_paginator.page(
            incoming_transfers_paginator.num_pages
        )

    return render(
        request,
        'pages/statistics_of_incoming_transfers.html',
        {'section': 'statistics_of_incoming_transfers',
         'page': page,
         'page_incoming_transfers': page_incoming_transfers}
    )


@login_required
def outbound_transfers_statistics(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    order_by = request.GET.get(
        'order_by'
    ) if request.GET.get('order_by') else 'id'

    try:
        outbound_transfers = list(
            request.user.accepted_transfers.filter(
                id__contains=search
            ).order_by(order+order_by)
        )
    except:
        outbound_transfers = list(
            request.user.accepted_transfers.all()
        )

    outbound_transfers_paginator = Paginator(outbound_transfers, 10)
    page = request.GET.get('page')

    try:
        page_outbound_transfers = outbound_transfers_paginator.page(
            page
        )
    except PageNotAnInteger:
        page_outbound_transfers = outbound_transfers_paginator.page(
            1
        )
    except EmptyPage:
        page_outbound_transfers = outbound_transfers_paginator.page(
            outbound_transfers_paginator.num_pages
        )
    return render(
        request,
        'pages/outbound_transfers_statistics.html',
        {'section': 'outbound_transfers_statistics',
         'page': page,
         'page_outbound_transfers': page_outbound_transfers}
    )


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            return render(request,
                          'registration/register_done.html')
    else:
        user_form = UserCreationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})
