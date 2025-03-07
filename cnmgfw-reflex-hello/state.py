# my_reflex_app/state.py
import os
import shutil
import subprocess
import http.server
import socketserver
import threading
import requests
import json
import time
import base64
import asyncio
from typing import List, Tuple
import reflex as rx

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')
        elif self.path == '/sub':
            try:
                with open(os.path.join(State.FILE_PATH, 'sub.txt'), 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Error reading file')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

class State(rx.State):
    # Environment variables
    FILE_PATH: str = os.environ.get('FILE_PATH', './temp')
    PROJECT_URL: str = os.environ.get('URL', '')
    INTERVAL_SECONDS: int = int(os.environ.get("TIME", 120))
    UUID: str = os.environ.get('UUID', 'abe2f2de-13ae-4f1f-bea5-d6c881ca3888')
    DOMAIN: str = os.environ.get('DOMAIN', 'n1.mcst.io')
    NAME: str = os.environ.get('NAME', 'Vls')
    PORT: int = int(os.environ.get('PORT', 3000))
    VPORT: int = int(os.environ.get('VPORT', 443))

    # State variables
    status: str = "Initializing..."
    sub_content: str = ""
    server_running: bool = False

    def __init__(self):
        super().__init__()
        # Initialize directory
        if not os.path.exists(self.FILE_PATH):
            os.makedirs(self.FILE_PATH)
            self.status = f"{self.FILE_PATH} has been created"
        else:
            self.status = f"{self.FILE_PATH} already exists"

        # Clean old files
        self.clean_old_files()

        # Start HTTP server
        self.start_http_server()

    def clean_old_files(self):
        paths_to_delete = ['list.txt', 'sub.txt', 'swith', 'web']
        for file in paths_to_delete:
            file_path = os.path.join(self.FILE_PATH, file)
            try:
                os.unlink(file_path)
                self.status = f"{file_path} has been deleted"
            except Exception:
                self.status = f"Skip Delete {file_path}"

    def start_http_server(self):
        if not self.server_running:
            self.httpd = socketserver.TCPServer(('', self.PORT), MyHandler)
            self.server_thread = threading.Thread(target=self.httpd.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.server_running = True
            self.status = "HTTP Server started"

    def generate_config(self):
        config = {
            "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
            "inbounds": [
                {
                    "port": self.VPORT,
                    "protocol": "vless",
                    "settings": {
                        "clients": [{"id": self.UUID, "flow": "xtls-rprx-vision"}],
                        "decryption": "none",
                        "fallbacks": [{"dest": 3001}, {"path": "/vless", "dest": 3002}]
                    },
                    "streamSettings": {"network": "tcp"}
                },
                {
                    "port": 3001,
                    "listen": "127.0.0.1",
                    "protocol": "vless",
                    "settings": {"clients": [{"id": self.UUID}], "decryption": "none"},
                    "streamSettings": {"network": "ws", "security": "none"}
                },
                {
                    "port": 3002,
                    "listen": "127.0.0.1",
                    "protocol": "vless",
                    "settings": {"clients": [{"id": self.UUID, "level": 0}], "decryption": "none"},
                    "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vless"}},
                    "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False}
                }
            ],
            "dns": {"servers": ["https+local://8.8.8.8/dns-query"]},
            "outbounds": [
                {"protocol": "freedom"},
                {
                    "tag": "WARP",
                    "protocol": "wireguard",
                    "settings": {
                        "secretKey": "YFYOAdbw1bKTHlNNi+aEjBM3BO7unuFC5rOkMRAz9XY=",
                        "address": ["172.16.0.2/32", "2606:4700:110:8a36:df92:102a:9602:fa18/128"],
                        "peers": [{"publicKey": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "allowedIPs": ["0.0.0.0/0", "::/0"], "endpoint": "162.159.193.10:2408"}],
                        "reserved": [78, 135, 76],
                        "mtu": 1280
                    }
                }
            ],
            "routing": {
                "domainStrategy": "AsIs",
                "rules": [{"type": "field", "domain": ["domain:openai.com", "domain:ai.com"], "outboundTag": "WARP"}]
            }
        }

        with open(os.path.join(self.FILE_PATH, 'config.json'), 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=2)

    def get_system_architecture(self) -> str:
        arch = os.uname().machine
        if 'arm' in arch or 'aarch64' in arch or 'arm64' in arch:
            return 'arm'
        return 'amd'

    def download_file(self, file_name: str, file_url: str):
        file_path = os.path.join(self.FILE_PATH, file_name)
        with requests.get(file_url, stream=True) as response, open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    def get_files_for_architecture(self, architecture: str) -> List[dict]:
        if architecture == 'arm':
            return [
                {'file_name': 'swith', 'file_url': 'https://github.com/eooce/test/releases/download/ARM/swith'},
                {'file_name': 'web', 'file_url': 'https://github.com/eooce/test/releases/download/ARM/web'},
            ]
        elif architecture == 'amd':
            return [
                {'file_name': 'swith', 'file_url': 'https://github.com/eooce/test/releases/download/bulid/swith'},
                {'file_name': 'web', 'file_url': 'https://github.com/eooce/test/releases/download/123/web'},
            ]
        return []

    def authorize_files(self, file_paths: List[str]):
        new_permissions = 0o775
        for relative_file_path in file_paths:
            absolute_file_path = os.path.join(self.FILE_PATH, relative_file_path)
            try:
                os.chmod(absolute_file_path, new_permissions)
                self.status = f"Empowerment success for {absolute_file_path}"
            except Exception as e:
                self.status = f"Empowerment failed for {absolute_file_path}: {e}"

    async def download_files_and_run(self):
        architecture = self.get_system_architecture()
        files_to_download = self.get_files_for_architecture(architecture)

        if not files_to_download:
            self.status = "Can't find a file for the current architecture"
            return

        for file_info in files_to_download:
            try:
                self.download_file(file_info['file_name'], file_info['file_url'])
                self.status = f"Downloaded {file_info['file_name']} successfully"
                yield
            except Exception as e:
                self.status = f"Download {file_info['file_name']} failed: {e}"
                yield

        files_to_authorize = ['./swith', './web']
        self.authorize_files(files_to_authorize)

        command = f"nohup {self.FILE_PATH}/web -c {self.FILE_PATH}/config.json >/dev/null 2>&1 &"
        try:
            subprocess.run(command, shell=True, check=True)
            self.status = 'Web service is running'
            yield
            await asyncio.sleep(1)
        except subprocess.CalledProcessError as e:
            self.status = f'Web running error: {e}'
            yield

        await asyncio.sleep(3)

    async def generate_links(self):
        meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
        meta_info = meta_info.stdout.split('"')
        ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()
        await asyncio.sleep(2)

        list_txt = f"""
vless://{self.UUID}@{self.DOMAIN}:{self.VPORT}?encryption=none&security=tls&sni={self.DOMAIN}&type=ws&host={self.DOMAIN}&path=%2Fvless%3Fed%3D2048#{self.NAME}-{ISP}
        """
        
        with open(os.path.join(self.FILE_PATH, 'list.txt'), 'w', encoding='utf-8') as list_file:
            list_file.write(list_txt)

        sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
        with open(os.path.join(self.FILE_PATH, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
            sub_file.write(sub_txt)

        try:
            with open(os.path.join(self.FILE_PATH, 'sub.txt'), 'rb') as file:
                self.sub_content = file.read().decode('utf-8')
            self.status = f"{self.FILE_PATH}/sub.txt saved successfully"
            yield
        except FileNotFoundError:
            self.status = "sub.txt not found"
            yield

        await asyncio.sleep(20)

        files_to_delete = ['list.txt', 'config.json']
        for file_to_delete in files_to_delete:
            file_path_to_delete = os.path.join(self.FILE_PATH, file_to_delete)
            try:
                os.remove(file_path_to_delete)
                self.status = f"{file_path_to_delete} has been deleted"
                yield
            except Exception as e:
                self.status = f"Error deleting {file_path_to_delete}: {e}"
                yield

        self.status = "App is running - Thank you for using this script!"
        yield

    async def start_server(self):
        self.status = "Starting server..."
        yield
        self.generate_config()
        async for update in self.download_files_and_run():
            yield update
        async for update in self.generate_links():
            yield update

    async def visit_project_page(self):
        if not self.PROJECT_URL or not self.INTERVAL_SECONDS:
            self.status = "URL or TIME variable is empty, Skipping visit web"
            yield
            return

        try:
            response = requests.get(self.PROJECT_URL)
            response.raise_for_status()
            self.status = "Page visited successfully"
            yield
            await asyncio.sleep(self.INTERVAL_SECONDS)
        except requests.exceptions.RequestException as error:
            self.status = f"Error visiting project page: {error}"
            yield
