from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import Server
from main.forms import CreateServerFrom


@login_required(login_url='/login/')
def servers_page(request):
    context = {
        'servers': Server.objects.filter(user=request.user)
    }
    return render(request, "servers.html", context)


@login_required(login_url='/login/')
def create_server_page(request):
    context = {'form': CreateServerFrom()}
    return render(request, "create_server.html", context)
