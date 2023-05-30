import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
import requests
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from ..models import *
from ..forms import *

AUTH_KEY = os.environ.get('AUTH_KEY')
SERVER_IP = os.environ.get('SERVER_IP')
SERVER_PORT = os.environ.get('SERVER_PORT')

SERVER_ADDR = str(SERVER_IP) + ':' + str(SERVER_PORT)

default_settings = {'version': '1.12.2',
                    'white_list': 'false',
                    'online_mode': 'false',
                    'pvp': 'true',
                    'allow_flight': 'true',
                    'spawn_animals': 'true',
                    'spawn_monsters': 'true',
                    'spawn_npcs': 'true',
                    'allow_nether': 'true',
                    'enable_command_block': 'true',
                    'max_players': '20',
                    'gamemode': 'survival',
                    'difficulty': 'normal'}


@login_required(login_url='/login/')
def start_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user or not server.paid:
        raise PermissionDenied
    docker_id = server.docker_id
    server.status = 'start'
    response = requests.get(f'http://{SERVER_ADDR}/start_server/{docker_id}',
                            params={'key': AUTH_KEY}, timeout=2)
    server.save()
    return JsonResponse({'status': response.text})


@login_required(login_url='/login/')
def restart_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user or not server.paid:
        raise PermissionDenied
    docker_id = server.docker_id
    server.status = 'start'
    response = requests.get(f'http://{SERVER_ADDR}/restart_server/{docker_id}',
                            params={'key': AUTH_KEY}, timeout=2)
    server.save()
    return JsonResponse({'status': response.text})


@login_required(login_url='/login/')
def stop_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    docker_id = server.docker_id
    server.status = 'stop'
    response = requests.get(f'http://{SERVER_ADDR}/stop_server/{docker_id}',
                            params={'key': AUTH_KEY}, timeout=2)
    server.save()
    return JsonResponse({'status': response.text})


@login_required(login_url='/login/')
def create_server(request):
    if request.method == 'POST':
        form = CreateServerFrom(request.POST)
        if form.is_valid():
            params = request.POST.dict()
            settings = default_settings.copy()
            settings['key'] = AUTH_KEY
            settings['plan'] = params['plan']
            response = requests.get(f'http://{SERVER_ADDR}/create_server/',
                                    params=settings, timeout=3)
            if response.status_code == 200:
                settings.pop('key')
                server = Server.objects.create(
                    name=params['name'], user=request.user,
                    docker_id=response.text[1:-1], plan=params['plan'], settings=settings)
                if server.plan == 'Free':
                    server.paid = True
                server.save()
    return redirect('/servers/')


@login_required(login_url='/login/')
def edit_server(request, server_id):
    if request.method == 'POST':
        server = get_object_or_404(Server, id=server_id)
        if server.user != request.user:
            raise PermissionDenied()
        form = SetServerSettingsForm(request.POST)
        if form.is_valid():
            params = request.POST.dict()
            params.pop('csrfmiddlewaretoken')
            settings = params.copy()
            params['key'] = AUTH_KEY
            params['version'] = server.settings['version']
            settings['version'] = server.settings['version']
            response = requests.get(f'http://{SERVER_ADDR}/edit_server/{server.docker_id}',
                                    params=params, timeout=2)
            if response.status_code == 200:
                server.docker_id = response.text[1:-1]
                server.settings = settings
                server.save()
    return redirect(f'/server/{server.id}/settings')


@login_required(login_url='/login/')
def edit_version_server(request, server_id):
    if request.method == 'POST':
        server = get_object_or_404(Server, id=server_id)
        if server.user != request.user:
            raise PermissionDenied()
        form = SetServerVersionForm(request.POST)
        if form.is_valid():
            params = request.POST.dict()
            params.pop('csrfmiddlewaretoken')
            settings = server.settings
            settings['key'] = AUTH_KEY
            settings['version'] = params['version']
            if 'CF_PAGE_URL' in settings:
                settings.pop('CF_PAGE_URL')
            response = requests.get(f'http://{SERVER_ADDR}/edit_server/{server.docker_id}',
                                    params=settings, timeout=2)
            settings.pop('key')
            if response.status_code == 200:
                server.docker_id = response.text[1:-1]
                server.settings = settings
                server.save()
    return redirect(f'/server/{server.id}/settings')


@login_required(login_url='/login/')
def run_command(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    docker_id = server.docker_id
    response = requests.get(f'http://{SERVER_ADDR}/run_command/{docker_id}',
                            params={'key': AUTH_KEY, 'command': request.GET['command']},
                            timeout=2)
    return JsonResponse({'status': response.text})


@login_required(login_url='/login/')
def delete_world(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    docker_id = server.docker_id
    response = requests.get(f'http://{SERVER_ADDR}/delete_world/{docker_id}',
                            params={'key': AUTH_KEY}, timeout=2)
    return JsonResponse({'status': response.text})


@login_required(login_url='/login/')
def set_modpack(request, server_id):
    if request.method == 'POST':
        server = get_object_or_404(Server, id=server_id)
        if server.user != request.user:
            raise PermissionDenied()
        form = SetModPackForm(request.POST)
        if form.is_valid():
            params = request.POST.dict()
            params.pop('csrfmiddlewaretoken')
            settings = server.settings
            settings['key'] = AUTH_KEY
            settings['CF_PAGE_URL'] = params['modpack']
            print(settings)
            response = requests.get(f'http://{SERVER_ADDR}/create_modpack_server/{server.docker_id}',
                                    params=settings, timeout=2)
            settings.pop('key')
            if response.status_code == 200:
                server.docker_id = response.text[1:-1]
                server.settings = settings
                server.save()
    return redirect(f'/server/{server.id}/settings')


@login_required(login_url='/login/')
def delete_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user != request.user:
        raise PermissionDenied()
    docker_id = server.docker_id
    response = requests.get(f'http://{SERVER_ADDR}/delete_server/{docker_id}',
                            params={'key': AUTH_KEY},
                            timeout=2)
    server.delete()
    return redirect(f'/servers')
