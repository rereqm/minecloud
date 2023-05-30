import asyncio
import os
import zipfile
from io import BytesIO
from threading import Thread
from fastapi import FastAPI, WebSocket, HTTPException, status, Request
from fastapi.responses import StreamingResponse
import servers_manager

app = FastAPI()
app.last_id = servers_manager.get_last_server_id() + 1

AUTH_KEY = os.environ.get('AUTH_KEY')
# а это папка уже в докере
BASE_DIR = os.getcwd()


def check_key(key):
    if key != AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


@app.get('/create_server/')
def create_server(key, request: Request):
    check_key(key)
    params = dict(request.query_params)
    print(params)
    server_id = servers_manager.create_server(app.last_id, params)
    app.last_id += 1
    return server_id


@app.get('/start_server/{server_id}')
def start_server(server_id: str, key):
    check_key(key)
    thread = Thread(
        target=servers_manager.start_container_by_id, args=(server_id,))
    thread.start()
    return 'Success'


@app.get('/stop_server/{server_id}')
def stop_server(server_id: str, key):
    check_key(key)
    thread = Thread(target=servers_manager.stop_container_by_id,
                    args=(server_id,))
    thread.start()
    return 'Success'


@app.get('/restart_server/{server_id}')
def restart_server(server_id: str, key):
    check_key(key)
    thread = Thread(
        target=servers_manager.restart_container_by_id, args=(server_id,))
    thread.start()
    return 'Success'


@app.get('/delete_server/{server_id}')
def delete_server(server_id: str, key):
    check_key(key)
    servers_manager.stop_container_by_id(server_id)
    servers_manager.delete_container_by_id(server_id)
    return 'Success'


@app.get('/run_command/{server_id}')
def run_command(server_id: str, command: str, key):
    check_key(key)
    response = servers_manager.run_command_on_server(server_id, command)
    return response


@app.get('/edit_server/{server_id}')
def edit_server(server_id, key, request: Request):
    check_key(key)
    params = dict(request.query_params)
    return servers_manager.edit_server(server_id, params)


@app.get('/delete_world/{server_id}')
def delete_world(server_id, key):
    check_key(key)
    servers_manager.delete_world_on_server(server_id)
    return 'Success'


@app.websocket('/ws/log/{server_id}')
async def websocket_endpoint(websocket: WebSocket, server_id):
    await websocket.accept()
    try:
        while True:
            logs = await all_log_reader(server_id)
            await websocket.send_text(logs)
            await asyncio.sleep(0.5)  # без этого сервер падает (почему - это не ко мне)
    except Exception as exception:
        print(exception)
    finally:
        await websocket.close()


async def all_log_reader(server_id):
    log_lines = []
    file_path = f'{BASE_DIR}/servers_data/' \
                f'{servers_manager.get_container_name(server_id)}/logs/latest.log'
    try:
        with open(file_path, encoding='utf-8') as file:
            for line in file.readlines()[-100:]:
                log_lines.append(f"<p>{line}</p>")
    except:
        pass
    return log_lines


@app.get('/download/{server_id}')
def download(server_id):
    server_name = servers_manager.get_container_name(server_id)
    zip_io = BytesIO()
    path = f'servers_data/{server_name}/world/'
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as world_zip:
        for root, dirs, files in os.walk(path):
            for file in files:
                world_zip.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file),
                                                os.path.join(path, '..')))

    response = StreamingResponse(iter([zip_io.getvalue()]), media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=world.zip"
    response.headers["Content-Type"] = 'application/force-download'
    return response


@app.get('/create_modpack_server/{server_id}')
def create_modpack_server(server_id, key, request: Request):
    check_key(key)
    params = dict(request.query_params)
    return servers_manager.create_modpack_server(server_id, params)