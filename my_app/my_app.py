import reflex as rx
import asyncio
from reflex.state import BaseState
import os
import re
import json
import time
import base64
import shutil
import platform
import subprocess
import threading
from threading import Thread
import requests

# Environment variables
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')
APP_URL = os.environ.get('APP_URL', '')
ENABLE_KEEP_ALIVE = os.environ.get('ENABLE_KEEP_ALIVE', 'false').lower() == 'true'
DATA_PATH = os.environ.get('DATA_PATH', './.cache')
SUBSCRIPTION_PATH = os.environ.get('SUBSCRIPTION_PATH', 'sub')
USER_ID = os.environ.get('USER_ID', 'ae1ea14e-5fc1-470a-bd0f-f1365c1ebc89')
SERVER_DOMAIN = os.environ.get('SERVER_DOMAIN', '')
SERVER_SECRET = os.environ.get('SERVER_SECRET', '')
SERVER_PORT = int(os.environ.get('SERVER_PORT', '8001'))
ENDPOINT_IP = os.environ.get('ENDPOINT_IP', 'cf.877774.xyz')
ENDPOINT_PORT = int(os.environ.get('ENDPOINT_PORT', '443'))
BOT_NAME = os.environ.get('BOT_NAME', 'xxx')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Global variables
core_executable_path = os.path.join(DATA_PATH, 'web')
connector_executable_path = os.path.join(DATA_PATH, 'bot')
subscription_file_path = os.path.join(DATA_PATH, 'sub.txt')
links_file_path = os.path.join(DATA_PATH, 'list.txt')
connector_log_path = os.path.join(DATA_PATH, 'boot.log')
config_file_path = os.path.join(DATA_PATH, 'config.json')

class State(BaseState):
    """The app state."""
    status: str = "Initializing..."
    subscription_content: str = ""
    is_running: bool = False

    async def start_service(self):
        if self.is_running:
            return
        self.is_running = True
        yield
        
        await self.run_setup()

    async def run_setup(self):
        self.status = "Deleting old nodes..."
        yield
        self.delete_nodes()

        self.status = "Cleaning up old files..."
        yield
        self.cleanup_old_files()

        self.status = "Creating directory..."
        yield
        self.create_directory()

        self.status = "Configuring tunnel..."
        yield
        self.configure_tunnel()

        self.status = "Downloading files..."
        yield
        await self.download_files_and_run()

        self.status = "Adding visit task..."
        yield
        self.add_visit_task()
        
        self.status = "Setup complete. Subscription is ready."
        yield
        
        if os.path.exists(subscription_file_path):
            with open(subscription_file_path, 'r') as f:
                self.subscription_content = f.read()
            yield

    def delete_nodes(self):
        try:
            if not WEBHOOK_URL:
                return

            if not os.path.exists(subscription_file_path):
                return

            try:
                with open(subscription_file_path, 'r') as file:
                    file_content = file.read()
            except:
                return None

            decoded = base64.b64decode(file_content).decode('utf-8')
            nodes = [line for line in decoded.split('\n') if any(protocol in line for protocol in ['vless://', 'vmess://', 'trojan://', 'hysteria2://', 'tuic://'])]

            if not nodes:
                return

            try:
                requests.post(f"{WEBHOOK_URL}/api/delete-nodes", 
                              data=json.dumps({"nodes": nodes}),
                              headers={"Content-Type": "application/json"})
            except:
                return None
        except Exception as e:
            print(f"Error in delete_nodes: {e}")
            return None

    def cleanup_old_files(self):
        paths_to_delete = ['web', 'bot', 'boot.log', 'list.txt']
        for file in paths_to_delete:
            file_path = os.path.join(DATA_PATH, file)
            try:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

    def create_directory(self):
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)

    def get_system_architecture(self):
        architecture = platform.machine().lower()
        if 'arm' in architecture or 'aarch64' in architecture:
            return 'arm'
        else:
            return 'amd'

    def download_file(self, file_name, file_url):
        file_path = os.path.join(DATA_PATH, file_name)
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return False

    def get_files_for_architecture(self, architecture):
        if architecture == 'arm':
            base_files = [
                {"fileName": "web", "fileUrl": "https://arm64.ssss.nyc.mn/web"},
                {"fileName": "bot", "fileUrl": "https://arm64.ssss.nyc.mn/2go"}
            ]
        else:
            base_files = [
                {"fileName": "web", "fileUrl": "https://amd64.ssss.nyc.mn/web"},
                {"fileName": "bot", "fileUrl": "https://amd64.ssss.nyc.mn/2go"}
            ]
        return base_files

    def authorize_files(self, file_paths):
        for relative_file_path in file_paths:
            absolute_file_path = os.path.join(DATA_PATH, relative_file_path)
            if os.path.exists(absolute_file_path):
                try:
                    os.chmod(absolute_file_path, 0o775)
                except Exception as e:
                    print(f"Empowerment failed for {absolute_file_path}: {e}")

    def configure_tunnel(self):
        if not SERVER_SECRET or not SERVER_DOMAIN:
            return

        if "TunnelSecret" in SERVER_SECRET:
            with open(os.path.join(DATA_PATH, 'tunnel.json'), 'w') as f:
                f.write(SERVER_SECRET)
            
            tunnel_id = SERVER_SECRET.split('"')[11]
            tunnel_yml = f"""
tunnel: {tunnel_id}
credentials-file: {os.path.join(DATA_PATH, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {SERVER_DOMAIN}
    service: http://localhost:{SERVER_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
"""
            with open(os.path.join(DATA_PATH, 'tunnel.yml'), 'w') as f:
                f.write(tunnel_yml)

    def exec_cmd(self, command):
        try:
            subprocess.Popen(
                command, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            print(f"Error executing command: {e}")

    async def download_files_and_run(self):
        architecture = self.get_system_architecture()
        files_to_download = self.get_files_for_architecture(architecture)
        
        if not files_to_download:
            self.status = "Can't find a file for the current architecture"
            return
        
        download_success = True
        for file_info in files_to_download:
            if not self.download_file(file_info["fileName"], file_info["fileUrl"]):
                download_success = False
        
        if not download_success:
            self.status = "Error downloading files"
            return
        
        files_to_authorize = ['web', 'bot']
        self.authorize_files(files_to_authorize)
        
        config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":SERVER_PORT ,"protocol":"vless","settings":{"clients":[{"id":USER_ID ,"flow":"xtls-rprx-vision",},],"decryption":"none","fallbacks":[{"dest":3001 },{"path":"/vless-argo","dest":3002 },{"path":"/vmess-argo","dest":3003 },{"path":"/trojan-argo","dest":3004 },],},"streamSettings":{"network":"tcp",},},{"port":3001 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID },],"decryption":"none"},"streamSettings":{"network":"ws","security":"none"}},{"port":3002 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3003 ,"listen":"127.0.0.1","protocol":"vmess","settings":{"clients":[{"id":USER_ID ,"alterId":0 }]},"streamSettings":{"network":"ws","wsSettings":{"path":"/vmess-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3004 ,"listen":"127.0.0.1","protocol":"trojan","settings":{"clients":[{"password":USER_ID },]},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/trojan-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},],"outbounds":[{"protocol":"freedom","tag": "direct" },{"protocol":"blackhole","tag":"block"}]}
        with open(config_file_path, 'w', encoding='utf-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=2)
        
        command = f"nohup {core_executable_path} -c {config_file_path} >/dev/null 2>&1 &"
        self.exec_cmd(command)
        
        if os.path.exists(connector_executable_path):
            if re.match(r'^[A-Z0-9a-z=]{120,250}$', SERVER_SECRET):
                args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {SERVER_SECRET}"
            elif "TunnelSecret" in SERVER_SECRET:
                args = f"tunnel --edge-ip-version auto --config {os.path.join(DATA_PATH, 'tunnel.yml')} run"
            else:
                args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {connector_log_path} --loglevel info --url http://localhost:{SERVER_PORT}"
            
            self.exec_cmd(f"nohup {connector_executable_path} {args} >/dev/null 2>&1 &")
        
        await asyncio.sleep(5)
        await self.extract_domains()

    async def extract_domains(self):
        server_domain = None

        if SERVER_SECRET and SERVER_DOMAIN:
            server_domain = SERVER_DOMAIN
            await self.generate_links(server_domain)
        else:
            try:
                with open(connector_log_path, 'r') as f:
                    file_content = f.read()
                
                lines = file_content.split('\n')
                server_domains = []
                
                for line in lines:
                    domain_match = re.search(r'https?://([^ ]*trycloudflare\.com)/?', line)
                    if domain_match:
                        domain = domain_match.group(1)
                        server_domains.append(domain)
                
                if server_domains:
                    server_domain = server_domains[0]
                    await self.generate_links(server_domain)
                else:
                    if os.path.exists(connector_log_path):
                        os.remove(connector_log_path)
                    
                    try:
                        self.exec_cmd('pkill -f "[b]ot" > /dev/null 2>&1')
                    except:
                        pass
                    
                    await asyncio.sleep(1)
                    args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {DATA_PATH}/boot.log --loglevel info --url http://localhost:{SERVER_PORT}'
                    self.exec_cmd(f'nohup {connector_executable_path} {args} >/dev/null 2>&1 &')
                    await asyncio.sleep(6)
                    await self.extract_domains()
            except Exception as e:
                print(f'Error reading connector log: {e}')

    def upload_nodes(self):
        if WEBHOOK_URL and APP_URL:
            subscription_url = f"{APP_URL}/{SUBSCRIPTION_PATH}"
            json_data = {
                "subscription": [subscription_url]
            }
            
            try:
                requests.post(
                    f"{WEBHOOK_URL}/api/add-subscriptions",
                    json=json_data,
                    headers={"Content-Type": "application/json"}
                )
            except Exception as e:
                pass
        
        elif WEBHOOK_URL:
            if not os.path.exists(links_file_path):
                return
            
            with open(links_file_path, 'r') as f:
                content = f.read()
            
            nodes = [line for line in content.split('\n') if any(protocol in line for protocol in ['vless://', 'vmess://', 'trojan://', 'hysteria2://', 'tuic://'])]
            
            if not nodes:
                return
            
            json_data = json.dumps({"nodes": nodes})
            
            try:
                requests.post(
                    f"{WEBHOOK_URL}/api/add-nodes",
                    data=json_data,
                    headers={"Content-Type": "application/json"}
                )
            except:
                return None
        else:
            return

    def send_telegram(self):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return
        
        try:
            with open(subscription_file_path, 'r') as f:
                message = f.read()
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            escaped_name = re.sub(r'([_*\[\]()~>#+=|{}.!\-])', r'\\\1', BOT_NAME)
            
            params = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": f"**{escaped_name} Update Notification**\n{message}",
                "parse_mode": "MarkdownV2"
            }
            
            requests.post(url, params=params)
        except Exception as e:
            print(f'Failed to send Telegram message: {e}')

    async def generate_links(self, server_domain):
        meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
        meta_info = meta_info.stdout.split('"')
        ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()

        await asyncio.sleep(2)
        VMESS = {"v": "2", "ps": f"{BOT_NAME}-{ISP}", "add": ENDPOINT_IP, "port": ENDPOINT_PORT, "id": USER_ID, "aid": "0", "scy": "none", "net": "ws", "type": "none", "host": server_domain, "path": "/vmess-argo?ed=2560", "tls": "tls", "sni": server_domain, "alpn": "", "fp": "chrome"}
     
        list_txt = f"""
vless://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?encryption=none&security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Fvless-argo%3Fed%3D2560#{BOT_NAME}-{ISP}
      
vmess://{ base64.b64encode(json.dumps(VMESS).encode('utf-8')).decode('utf-8')}

trojan://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Ftrojan-argo%3Fed%3D2560#{BOT_NAME}-{ISP}
        """
        
        with open(links_file_path, 'w', encoding='utf-8') as list_file:
            list_file.write(list_txt)

        sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
        with open(subscription_file_path, 'w', encoding='utf-8') as sub_file:
            sub_file.write(sub_txt)
            
        self.send_telegram()
        self.upload_nodes()
      
        return sub_txt   
     
    def add_visit_task(self):
        if not ENABLE_KEEP_ALIVE or not APP_URL:
            return
        
        try:
            requests.post(
                'https://keep.gvrander.eu.org/add-url',
                json={"url": APP_URL},
                headers={"Content-Type": "application/json"}
            )
        except Exception as e:
            print(f'Failed to add URL: {e}')

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Reflex Service Manager", size="9"),
            rx.button(
                "Start Service",
                on_click=State.start_service,
                is_disabled=State.is_running,
                size="4",
            ),
            rx.text(State.status, size="6"),
            rx.cond(
                State.subscription_content,
                rx.text_area(value=State.subscription_content, is_read_only=True, width="100%", height="200px")
            ),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )

app = rx.App()
app.add_page(index)
