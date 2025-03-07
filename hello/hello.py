import reflex as rx
import os
import shutil
import subprocess
import requests
import json
import time
import base64
import platform
from typing import List, Dict
import asyncio

# Reflex 应用状态
class AppState(rx.State):
    file_path: str = os.environ.get('FILE_PATH', './temp')
    project_url: str = os.environ.get('URL', '')
    interval_seconds: int = int(os.environ.get("TIME", 120))
    uuid: str = os.environ.get('UUID', 'abe2f2de-13ae-4f1f-bea5-d6c881ca3888')
    domain: str = os.environ.get('DOMAIN', 'n1.mcst.io')
    name: str = os.environ.get('NAME', 'Vls')
    port: int = int(os.environ.get('PORT', 3000))
    vport: int = int(os.environ.get('VPORT', 443))
    sub_content: str = ""
    is_running: bool = False

    def setup(self):
        """初始化应用"""
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
            print(f"{self.file_path} has been created")
        else:
            print(f"{self.file_path} already exists")
        self.clean_old_files()
        self.start_server()

    def clean_old_files(self):
        """清理旧文件"""
        paths_to_delete = ['list.txt', 'sub.txt', 'swith', 'web']
        for file in paths_to_delete:
            file_path = os.path.join(self.file_path, file)
            try:
                os.unlink(file_path)
                print(f"{file_path} has been deleted")
            except Exception as e:
                print(f"Skip Delete {file_path}")

    def generate_config(self):
        """生成 VLESS 配置文件"""
        config = {
            "log": {"access": "/dev/null", "error": "/dev/null", "loglevel": "none"},
            "inbounds": [
                {
                    "port": self.vport,
                    "protocol": "vless",
                    "settings": {
                        "clients": [{"id": self.uuid, "flow": "xtls-rprx-vision"}],
                        "decryption": "none",
                        "fallbacks": [{"dest": 3001}, {"path": "/vless", "dest": 3002}],
                    },
                    "streamSettings": {"network": "tcp"},
                },
                {
                    "port": 3001,
                    "listen": "127.0.0.1",
                    "protocol": "vless",
                    "settings": {"clients": [{"id": self.uuid}], "decryption": "none"},
                    "streamSettings": {"network": "ws", "security": "none"},
                },
                {
                    "port": 3002,
                    "listen": "127.0.0.1",
                    "protocol": "vless",
                    "settings": {"clients": [{"id": self.uuid, "level": 0}], "decryption": "none"},
                    "streamSettings": {"network": "ws", "security": "none", "wsSettings": {"path": "/vless"}},
                    "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "metadataOnly": False},
                },
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
                        "mtu": 1280,
                    },
                },
            ],
            "routing": {
                "domainStrategy": "AsIs",
                "rules": [{"type": "field", "domain": ["domain:openai.com", "domain:ai.com"], "outboundTag": "WARP"}],
            },
        }
        with open(os.path.join(self.file_path, 'config.json'), 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=2)

    def get_system_architecture(self) -> str:
        """检测系统架构"""
        arch = platform.machine().lower()
        if 'arm' in arch or 'aarch64' in arch or 'arm64' in arch:
            return 'arm'
        return 'amd'

    def get_files_for_architecture(self, architecture: str) -> List[Dict[str, str]]:
        """根据架构返回文件信息"""
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

    def download_file(self, file_name: str, file_url: str):
        """下载文件"""
        file_path = os.path.join(self.file_path, file_name)
        with requests.get(file_url, stream=True) as response, open(file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)

    def authorize_files(self, file_paths: List[str]):
        """授权文件"""
        new_permissions = 0o775
        for relative_file_path in file_paths:
            absolute_file_path = os.path.join(self.file_path, relative_file_path)
            try:
                os.chmod(absolute_file_path, new_permissions)
                print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
            except Exception as e:
                print(f"Empowerment failed for {absolute_file_path}: {e}")

    def download_files_and_run(self):
        """下载并运行文件"""
        architecture = self.get_system_architecture()
        files_to_download = self.get_files_for_architecture(architecture)
        if not files_to_download:
            print("Can't find a file for the current architecture")
            return

        for file_info in files_to_download:
            try:
                self.download_file(file_info['file_name'], file_info['file_url'])
                print(f"Downloaded {file_info['file_name']} successfully")
            except Exception as e:
                print(f"Download {file_info['file_name']} failed: {e}")

        files_to_authorize = ['swith', 'web']
        self.authorize_files(files_to_authorize)

        command = f"nohup {self.file_path}/web -c {self.file_path}/config.json >/dev/null 2>&1 &"
        try:
            subprocess.run(command, shell=True, check=True)
            print('web is running')
            time.sleep(1)
        except subprocess.CalledProcessError as e:
            print(f'web running error: {e}')

    def generate_links(self):
        """生成链接和订阅内容"""
        meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
        meta_info = meta_info.stdout.split('"')
        isp = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()
        time.sleep(2)

        list_txt = f"""
vless://{self.uuid}@{self.domain}:{self.vport}?encryption=none&security=tls&sni={self.domain}&type=ws&host={self.domain}&path=%2Fvless%3Fed%3D2048#{self.name}-{isp}
        """
        with open(os.path.join(self.file_path, 'list.txt'), 'w', encoding='utf-8') as list_file:
            list_file.write(list_txt)

        sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
        with open(os.path.join(self.file_path, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
            sub_file.write(sub_txt)

        try:
            with open(os.path.join(self.file_path, 'sub.txt'), 'rb') as file:
                self.sub_content = file.read().decode('utf-8')
            print(f"\n{self.sub_content}")
        except FileNotFoundError:
            print("sub.txt not found")

        print(f'{self.file_path}/sub.txt saved successfully')
        time.sleep(20)

        files_to_delete = ['list.txt', 'config.json']
        for file_to_delete in files_to_delete:
            file_path_to_delete = os.path.join(self.file_path, file_to_delete)
            try:
                os.remove(file_path_to_delete)
                print(f"{file_path_to_delete} has been deleted")
            except Exception as e:
                print(f"Error deleting {file_path_to_delete}: {e}")

        self.is_running = True

    def start_server(self):
        """启动服务"""
        self.generate_config()
        self.download_files_and_run()
        self.generate_links()

    async def visit_project_page(self):
        """定期访问项目页面"""
        while True:
            if self.project_url and self.interval_seconds:
                try:
                    response = requests.get(self.project_url)
                    response.raise_for_status()
                    print("Page visited successfully")
                except requests.exceptions.RequestException as error:
                    print(f"Error visiting project page: {error}")
            await asyncio.sleep(self.interval_seconds)

# 前端页面
def index() -> rx.Component:
    return rx.vstack(
        rx.text("Hello, World!", font_size="2em"),
        rx.cond(
            AppState.is_running,
            rx.text(f"Subscription: {AppState.sub_content}", font_size="1.2em"),
            rx.text("Server is starting...", font_size="1.2em")
        ),
        rx.button("Refresh", on_click=AppState.setup),
        align_items="center",
        spacing="4",
    )

# Reflex 应用配置
app = rx.App(state=AppState)
app.add_page(index, route="/", on_load=AppState.setup)

# 添加 /sub 路由
@app.api.get("/sub")
async def get_sub():
    file_path = os.path.join(AppState.file_path, 'sub.txt')
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        return rx.Response(content, mimetype="text/plain; charset=utf-8")
    except FileNotFoundError:
        return rx.Response("Error reading file", status_code=500)

# 启动时运行后台任务
@app.api.on_startup
async def startup():
    asyncio.create_task(AppState().visit_project_page())
