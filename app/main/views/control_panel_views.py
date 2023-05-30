import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from ..models import Server
from ..forms import SetServerSettingsForm, BudgetServerPaymentForm, BoostServerPaymentForm
from django.contrib import messages

SERVER_IP = os.environ.get('SERVER_IP')
SERVER_PORT = os.environ.get('SERVER_PORT')

SERVER_ADDR = str(SERVER_IP) + ':' + str(SERVER_PORT)


@login_required(login_url='/login/')
def console_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    context = {'server': server,
               'SERVER_ADDR': SERVER_ADDR,
               'WEBSOCKET': SERVER_IP,
               'SERVER_IP': '77.232.137.182',
               'SERVER_PORT': server_id+25564,
               }
    return render(request, 'server_console.html', context)


@login_required(login_url='/login/')
def settings_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    if server.status == 'start':
        return redirect(f'/server/{server.id}/console')
    if 'CF_PAGE_URL' in server.settings:
        server_type = f'modepack {server.settings["CF_PAGE_URL"]}'
    else:
        server_type = f'vanilla {server.settings["version"]}'
    context = {'form': SetServerSettingsForm(server.settings), 'server': server, 'type': server_type}
    return render(request, "server_settings.html", context)


@login_required(login_url='/login/')
def world_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    context = {'server': server,
               'SERVER_IP': SERVER_IP}
    return render(request, "server_world.html", context)


@login_required(login_url='/login/')
def payment_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    if server.plan == 'Free':
        return redirect(f'/server/{server.id}/console')
    if request.method == 'GET':
        context = {'server': server}
        if server.plan == 'Budget':
            context['form'] = BudgetServerPaymentForm()
        elif server.plan == 'Boost':
            context['form'] = BoostServerPaymentForm()
        return render(request, "server_payment.html", context)
    elif request.method == 'POST':
        data = request.POST.dict()
        if server.plan == 'Budget':
            form = BudgetServerPaymentForm(request.POST)
            data['one_day_cost'] = 5
        elif server.plan == 'Boost':
            form = BoostServerPaymentForm(request.POST)
            data['one_day_cost'] = 10
        print(form.is_valid())
        print(data['one_day_cost']*data['days'], data['total'])
        if form.is_valid():
            if int(data['one_day_cost'])*int(data['days']) == int(data['total']):
                if request.user.money >= int(data['total']):
                    server.remaining_days += int(data['days'])
                    server.paid = True
                    request.user.money -= float(data['total'])
                    server.save()
                    request.user.save()
                    messages.success(request, 'Success!')
                else:
                    messages.error(request, 'Not enough money')
            else:
                messages.error(request, 'Error!')
        else:
            messages.error(request, 'Error!')
        return redirect(f'/server/{server.id}/payment')


@login_required(login_url='/login/')
def delete_page(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    if request.method == 'GET':
        context = {'server': server}
        return render(request, "server_delete.html", context)