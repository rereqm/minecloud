import os
import shutil
import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')
# это папка на хосте НЕ НА ДОКЕРЕ!
BASE_DIR = '/minecloud_ver_2/servers_controller'

DEFAULT_MODPACK_URL = 'https://www.curseforge.com/minecraft/modpacks/'


def create_server(server_id, params=None):
    if params is None:
        params = {}
    my_env = {
        'EULA': True if 'eula' not in params else params['eula'],
        'ONLINE_MODE': params['online_mode'],
        'TYPE': 'VANILLA' if 'type' not in params else params['type'],
        'VERSION': '1.12.2' if 'version' not in params else params['version'],
        'MODE': params['gamemode'],
        'MAX_PLAYERS': params['max_players'],
        'DIFFICULTY': params['difficulty'],
        'ENABLE_WHITELIST': params['white_list'],
        'PVP': params['pvp'],
        'ALLOW_FLIGHT': params['allow_flight'],
        'SPAWN_ANIMALS': params['spawn_animals'],
        'SPAWN_MONSTERS': params['spawn_monsters'],
        'SPAWN_NPCS': params['spawn_npcs'],
        'ALLOW_NETHER': params['allow_nether'],
        'MOTD': 'Server runs by MineCloud' if 'motd' not in params else params['motd'],
        'ENABLE_RCON': False
    }
    if 'CF_PAGE_URL' in params:
        my_env['TYPE'] = 'AUTO_CURSEFORGE'
        my_env['CF_API_KEY'] = '$2a$10$LjhbUfJtk/S0Njq8qJLS3uDKpOi6IKA5S/v6JkaPb5UCsMp2EyNq6'
        my_env['CF_PAGE_URL'] = DEFAULT_MODPACK_URL + params['CF_PAGE_URL']
        image = 'itzg/minecraft-server:java8-jdk'
    else:
        image = 'itzg/minecraft-server'
    container = client.containers.create(image=image,
                                         name=f'minecraft_server{server_id}',
                                         ports={
                                             '25565/tcp': 25564 + server_id},
                                         volumes={
                                             f'{BASE_DIR}/servers_data/minecraft_server{server_id}':
                                                 {'bind': '/data', 'mode': 'rw'}
                                         },
                                         detach=True,
                                         environment=my_env,
                                         mem_limit='3g')
    os.makedirs(f'servers_data/minecraft_server{server_id}/logs', 0o755, exist_ok=True)
    with open(f'servers_data/minecraft_server{server_id}/logs/latest.log', 'w+', encoding='utf-8'):
        pass
    return container.id


def container_list():
    return client.containers.list(all=True, filters={'name': 'minecraft_server'})


def get_container_by_id(server_id):
    return client.containers.get(server_id)


def stop_container_by_id(server_id):
    container = get_container_by_id(server_id)
    container.stop(timeout=10)
    return 0


def start_container_by_id(server_id):
    container = get_container_by_id(server_id)
    container.start()
    return 0


def restart_container_by_id(server_id):
    container = get_container_by_id(server_id)
    container.restart(timeout=10)
    return 0


def get_container_name(server_id):
    container = get_container_by_id(server_id)
    return container.name


def delete_container_by_id(server_id):
    container = get_container_by_id(server_id)
    container.remove()
    return 0


def get_logs_container_by_id(server_id):
    container = get_container_by_id(server_id)
    return container.logs().decode()


def get_last_server_id():
    if len(container_list()) == 0:
        return 0
    return int(container_list()[0].name[16:])


def run_command_on_server(server_id, command):
    container = get_container_by_id(server_id)
    return container.exec_run(['mc-send-to-console', command])


def edit_server(server_id, params):
    container = get_container_by_id(server_id)
    old_id = int(container.name[16:])
    config = container.attrs['Config']['Env']
    old_version = config[3][8:]
    container.remove()
    if old_version != params['version']:
        shutil.rmtree(f'servers_data/minecraft_server{old_id}/world/', ignore_errors=True)
    dir_name = f'servers_data/minecraft_server{old_id}/'
    new_container_id = create_server(old_id, params)
    return new_container_id


def delete_world_on_server(server_id):
    server_name = get_container_name(server_id)
    shutil.rmtree(f'servers_data/{server_name}/world/', ignore_errors=True)


def create_modpack_server(server_id, params):
    container = get_container_by_id(server_id)
    old_id = int(container.name[16:])
    container.remove()
    shutil.rmtree(f'servers_data/minecraft_server{old_id}/', ignore_errors=True)

    new_container_id = create_server(old_id, params)
    return new_container_id
