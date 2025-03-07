import os
import re
import shutil
import subprocess
import threading
import requests
import json
import time
import base64

# Environment variables setup
FILE_PATH = os.environ.get('FILE_PATH', './tmp')
PROJECT_URL = os.environ.get('URL', '')
INTERVAL_SECONDS = int(os.environ.get("TIME", 120))
UUID = os.environ.get('UUID', 'dd0ba961-6982-40dd-bff5-b1e3397cc39f')
ARGO_DOMAIN = os.environ.get('ARGO_DOMAIN', '')
ARGO_AUTH = os.environ.get('ARGO_AUTH', '')
ARGO_PORT = int(os.environ.get('ARGO_PORT', 8001))
CFIP = os.environ.get('CFIP', 'www.visa.com.tw')
CFPORT = int(os.environ.get('CFPORT', 443))
NAME = os.environ.get('NAME', 'ReflexCloud')
PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000)

# Directory setup
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    print(f"{FILE_PATH} has been created")
else:
    print(f"{FILE_PATH} already exists")

# Clean old files
paths_to_delete = ['boot.log', 'list.txt', 'sub.txt', 'npm', 'web', 'bot', 'tunnel.yml', 'tunnel.json']
for file in paths_to_delete:
    file_path = os.path.join(FILE_PATH, file)
    try:
        os.unlink(file_path)
        print(f"{file_path} has been deleted")
    except Exception as e:
        print(f"Skip Delete {file_path}")

# Generate xr-ay config file
def generate_config():
    config = {
        "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
        "inbounds": [
            {
                "port": ARGO_PORT,
                "protocol": "vless",
                "settings": {
                    "clients": [{"id": UUID, "flow": "xtls-rprx-vision"}],
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
            # ... (rest of the inbounds config remains the same)
        ],
        "dns": {"servers": ["https+local://8.8.8.8/dns-query"]},
        "outbounds": [
            {"protocol": "freedom", "tag": "direct"},
            {"protocol": "blackhole", "tag": "block"}
        ]
    }
    with open(os.path.join(FILE_PATH, 'config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)

# System architecture detection
def get_system_architecture():
    arch = os.uname().machine
    if 'arm' in arch or 'aarch64' in arch or 'arm64' in arch:
        return 'arm'
    else:
        return 'amd'

# File download utility
def download_file(file_name, file_url):
    file_path = os.path.join(FILE_PATH, file_name)
    with requests.get(file_url, stream=True) as response, open(file_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

# Architecture-specific files
def get_files_for_architecture(architecture):
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

# Authorize files
def authorize_files(file_paths):
    new_permissions = 0o775
    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        try:
            os.chmod(absolute_file_path, new_permissions)
            print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
        except Exception as e:
            print(f"Empowerment failed for {absolute_file_path}: {e}")

# Cloudflare args
def get_cloud_flare_args():
    processed_auth = ARGO_AUTH
    try:
        auth_data = json.loads(ARGO_AUTH)
        if all(k in auth_data for k in ['TunnelSecret', 'AccountTag', 'TunnelID']):
            processed_auth = 'TunnelSecret'
    except json.JSONDecodeError:
        pass

    if not processed_auth and not ARGO_DOMAIN:
        return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{ARGO_PORT}'
    elif processed_auth == 'TunnelSecret':
        return f'tunnel --edge-ip-version auto --config {FILE_PATH}/tunnel.yml run'
    elif processed_auth and ARGO_DOMAIN and 120 <= len(processed_auth) <= 250:
        return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {processed_auth}'
    else:
        return f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{ARGO_PORT}'

# Argo config
def argo_config():
    if not ARGO_AUTH or not ARGO_DOMAIN:
        print("ARGO_DOMAIN or ARGO_AUTH is empty, use quick Tunnels")
        return

    if 'TunnelSecret' in ARGO_AUTH:
        with open(os.path.join(FILE_PATH, 'tunnel.json'), 'w') as file:
            file.write(ARGO_AUTH)
        tunnel_yaml = f"""
tunnel: {ARGO_AUTH.split('"')[11]}
credentials-file: {os.path.join(FILE_PATH, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {ARGO_DOMAIN}
    service: http://localhost:{ARGO_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
  """
        with open(os.path.join(FILE_PATH, 'tunnel.yml'), 'w') as file:
            file.write(tunnel_yaml)
    else:
        print("Use token connect to tunnel")

# Extract domains and generate links
def extract_domains():
    argo_domain = ARGO_DOMAIN if ARGO_AUTH and ARGO_DOMAIN else ''
    if not argo_domain:
        try:
            with open(os.path.join(FILE_PATH, 'boot.log'), 'r', encoding='utf-8') as file:
                content = file.read()
                match = re.search(r'https://([^ ]+\.trycloudflare\.com)', content)
                if match:
                    argo_domain = match.group(1)
                    print('ArgoDomain:', argo_domain)
                    generate_links(argo_domain)
                else:
                    # Retry logic (simplified for brevity)
                    print('ArgoDomain not found, implement retry logic here if needed')
        except Exception as e:
            print(f"Error reading boot.log: {e}")
    else:
        generate_links(argo_domain)

def generate_links(argo_domain):
    meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
    meta_info = meta_info.stdout.split('"')
    ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()

    VMESS = {
        "v": "2", "ps": f"{NAME}-{ISP}", "add": CFIP, "port": CFPORT, "id": UUID,
        "aid": "0", "scy": "none", "net": "ws", "type": "none", "host": argo_domain,
        "path": "/vmess-argo?ed=2048", "tls": "tls", "sni": argo_domain, "alpn": ""
    }

    list_txt = f"""
vless://{UUID}@{CFIP}:{CFPORT}?encryption=none&security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Fvless-argo%3Fed%3D2048#{NAME}-{ISP}
vmess://{base64.b64encode(json.dumps(VMESS).encode('utf-8')).decode('utf-8')}
trojan://{UUID}@{CFIP}:{CFPORT}?security=tls&sni={argo_domain}&type=ws&host={argo_domain}&path=%2Ftrojan-argo%3Fed%3D2048#{NAME}-{ISP}
    """
    with open(os.path.join(FILE_PATH, 'list.txt'), 'w', encoding='utf-8') as list_file:
        list_file.write(list_txt)

    sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
    with open(os.path.join(FILE_PATH, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
        sub_file.write(sub_txt)

# Download and run files
def download_files_and_run():
    architecture = get_system_architecture()
    files_to_download = get_files_for_architecture(architecture)
    for file_info in files_to_download:
        try:
            download_file(file_info['file_name'], file_info['file_url'])
            print(f"Downloaded {file_info['file_name']} successfully")
        except Exception as e:
            print(f"Download {file_info['file_name']} failed: {e}")

    authorize_files(['npm', 'web', 'bot'])
    subprocess.run(f"nohup {FILE_PATH}/web -c {FILE_PATH}/config.json >/dev/null 2>&1 &", shell=True)
    if os.path.exists(os.path.join(FILE_PATH, 'bot')):
        args = get_cloud_flare_args()
        subprocess.run(f"nohup {FILE_PATH}/bot {args} >/dev/null 2>&1 &", shell=True)

def start_server():
    generate_config()
    argo_config()
    download_files_and_run()
    extract_domains()

# Background thread for server start
def run_server_in_background():
    threading.Thread(target=start_server, daemon=True).start()

# Periodic project page visit
has_logged_empty_message = False

def visit_project_page():
    global has_logged_empty_message
    try:
        if not PROJECT_URL or not INTERVAL_SECONDS:
            if not has_logged_empty_message:
                print("URL or TIME variable is empty, Skipping visit web")
                has_logged_empty_message = True
            return
        response = requests.get(PROJECT_URL)
        response.raise_for_status()
        print("Page visited successfully")
    except requests.exceptions.RequestException as error:
        print(f"Error visiting project page: {error}")
