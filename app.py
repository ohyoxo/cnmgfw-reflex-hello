import reflex as rx
import os
import re
import json
import time
import base64
import shutil
import asyncio
import requests
import platform
import subprocess
from fastapi import Response
from fastapi.responses import PlainTextResponse

# --- Environment Variables ---
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

# --- Global Variables ---
core_executable_path = os.path.join(DATA_PATH, 'web')
connector_executable_path = os.path.join(DATA_PATH, 'bot')
subscription_file_path = os.path.join(DATA_PATH, 'sub.txt')
links_file_path = os.path.join(DATA_PATH, 'list.txt')
connector_log_path = os.path.join(DATA_PATH, 'boot.log')
config_file_path = os.path.join(DATA_PATH, 'config.json')

# --- Helper Functions (Original Logic) ---
# Note: These functions are kept as close to the original as possible.
# The `print` statements will be redirected to the state logger.

def exec_cmd(command):
    try:
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        return stdout + stderr
    except Exception as e:
        return f"Error executing command: {e}"

def get_system_architecture():
    architecture = platform.machine().lower()
    return 'arm' if 'arm' in architecture or 'aarch64' in architecture else 'amd'

class AppState(rx.State):
    logs: list[str] = []
    is_initialized: bool = False
    subscription_url: str = f"/{SUBSCRIPTION_PATH}"

    def _log(self, message: str):
        self.logs.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        print(message)

    async def _cleanup_task(self):
        self._log("Cleanup task scheduled in 90 seconds.")
        await asyncio.sleep(90)
        files_to_delete = [connector_log_path, config_file_path, links_file_path, core_executable_path, connector_executable_path]
        for file in files_to_delete:
            try:
                if os.path.exists(file):
                    if os.path.isdir(file): shutil.rmtree(file)
                    else: os.remove(file)
            except Exception as e:
                self._log(f"Cleanup error for {file}: {e}")
        self._log("Cleanup complete. App is running.")
        self._log("Thank you for using this script, enjoy!")

    def _create_directory(self):
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            self._log(f"{DATA_PATH} is created")
        else:
            self._log(f"{DATA_PATH} already exists")

    def _delete_nodes(self):
        try:
            if not WEBHOOK_URL or not os.path.exists(subscription_file_path): return
            with open(subscription_file_path, 'r') as file: file_content = file.read()
            decoded = base64.b64decode(file_content).decode('utf-8')
            nodes = [line for line in decoded.split('\n') if any(p in line for p in ['vless://', 'vmess://', 'trojan://'])]
            if nodes: requests.post(f"{WEBHOOK_URL}/api/delete-nodes", data=json.dumps({"nodes": nodes}), headers={"Content-Type": "application/json"})
        except Exception as e: self._log(f"Error in delete_nodes: {e}")

    def _cleanup_old_files(self):
        for file in ['web', 'bot', 'boot.log', 'list.txt']:
            path = os.path.join(DATA_PATH, file)
            try:
                if os.path.exists(path):
                    if os.path.isdir(path): shutil.rmtree(path)
                    else: os.remove(path)
            except Exception as e: self._log(f"Error removing {path}: {e}")

    def _download_file(self, file_name, file_url):
        file_path = os.path.join(DATA_PATH, file_name)
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192): f.write(chunk)
            self._log(f"Download {file_name} successfully")
            return True
        except Exception as e:
            if os.path.exists(file_path): os.remove(file_path)
            self._log(f"Download {file_name} failed: {e}")
            return False

    def _authorize_files(self, file_paths):
        for path in file_paths:
            abs_path = os.path.join(DATA_PATH, path)
            if os.path.exists(abs_path):
                try:
                    os.chmod(abs_path, 0o775)
                    self._log(f"Empowerment success for {abs_path}: 775")
                except Exception as e: self._log(f"Empowerment failed for {abs_path}: {e}")

    def _configure_tunnel(self):
        if not SERVER_SECRET or not SERVER_DOMAIN:
            self._log("SERVER_DOMAIN or SERVER_SECRET empty, use quick tunnels")
            return
        if "TunnelSecret" in SERVER_SECRET:
            with open(os.path.join(DATA_PATH, 'tunnel.json'), 'w') as f: f.write(SERVER_SECRET)
            tunnel_id = SERVER_SECRET.split('"')[11]
            tunnel_yml = f"tunnel: {tunnel_id}\ncredentials-file: {os.path.join(DATA_PATH, 'tunnel.json')}\nprotocol: http2\n\ningress:\n  - hostname: {SERVER_DOMAIN}\n    service: http://localhost:{SERVER_PORT}\n    originRequest:\n      noTLSVerify: true\n  - service: http_status:404"
            with open(os.path.join(DATA_PATH, 'tunnel.yml'), 'w') as f: f.write(tunnel_yml)
        else: self._log("Use token connect to tunnel, please set {SERVER_PORT} in cloudflare")

    def _upload_nodes(self):
        try:
            if WEBHOOK_URL and APP_URL:
                requests.post(f"{WEBHOOK_URL}/api/add-subscriptions", json={"subscription": [f"{APP_URL}/{SUBSCRIPTION_PATH}"]}, headers={"Content-Type": "application/json"})
                self._log('Subscription uploaded successfully')
            elif WEBHOOK_URL and os.path.exists(links_file_path):
                with open(links_file_path, 'r') as f: content = f.read()
                nodes = [line for line in content.split('\n') if any(p in line for p in ['vless://', 'vmess://', 'trojan://'])]
                if nodes:
                    requests.post(f"{WEBHOOK_URL}/api/add-nodes", data=json.dumps({"nodes": nodes}), headers={"Content-Type": "application/json"})
                    self._log('Nodes uploaded successfully')
        except Exception as e: self._log(f"Node upload failed: {e}")

    def _send_telegram(self):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
        try:
            with open(subscription_file_path, 'r') as f: message = f.read()
            escaped_name = re.sub(r'([_*\[\]()~>#+=|{}.!\-])', r'\\\1', BOT_NAME)
            params = {"chat_id": TELEGRAM_CHAT_ID, "text": f"**{escaped_name} Update Notification**\n{message}", "parse_mode": "MarkdownV2"}
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
            self._log('Telegram message sent successfully')
        except Exception as e: self._log(f'Failed to send Telegram message: {e}')

    async def _generate_links(self, server_domain):
        meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True).stdout.split('"')
        ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()
        VMESS = {"v": "2", "ps": f"{BOT_NAME}-{ISP}", "add": ENDPOINT_IP, "port": ENDPOINT_PORT, "id": USER_ID, "aid": "0", "scy": "none", "net": "ws", "type": "none", "host": server_domain, "path": "/vmess-argo?ed=2560", "tls": "tls", "sni": server_domain, "alpn": "", "fp": "chrome"}
        list_txt = f"vless://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?encryption=none&security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Fvless-argo%3Fed%3D2560#{BOT_NAME}-{ISP}\n\nvmess://{base64.b64encode(json.dumps(VMESS).encode('utf-8')).decode('utf-8')}\n\ntrojan://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Ftrojan-argo%3Fed%3D2560#{BOT_NAME}-{ISP}"
        with open(links_file_path, 'w', encoding='utf-8') as f: f.write(list_txt)
        sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
        with open(subscription_file_path, 'w', encoding='utf-8') as f: f.write(sub_txt)
        self._log(f"{DATA_PATH}/sub.txt saved successfully")
        self._send_telegram()
        self._upload_nodes()

    async def _extract_domains(self):
        if SERVER_SECRET and SERVER_DOMAIN:
            self._log(f'Using provided SERVER_DOMAIN: {SERVER_DOMAIN}')
            await self._generate_links(SERVER_DOMAIN)
            return
        
        await asyncio.sleep(8) # Wait for log file
        try:
            with open(connector_log_path, 'r') as f: content = f.read()
            domains = re.findall(r'https?://([^ ]*trycloudflare\.com)', content)
            if domains:
                self._log(f'Found ServerDomain: {domains[0]}')
                await self._generate_links(domains[0])
            else:
                self._log('ServerDomain not found in logs.')
        except Exception as e: self._log(f'Error reading connector log: {e}')

    def _add_visit_task(self):
        if not ENABLE_KEEP_ALIVE or not APP_URL:
            self._log("Skipping keep-alive task.")
            return
        try:
            requests.post('https://keep.gvrander.eu.org/add-url', json={"url": APP_URL}, headers={"Content-Type": "application/json"})
            self._log('Keep-alive task added successfully')
        except Exception as e: self._log(f'Failed to add keep-alive URL: {e}')

    async def initialize_service(self):
        if self.is_initialized:
            self._log("Service already initialized.")
            return
        
        self._log("--- Starting Service Initialization ---")
        self._delete_nodes()
        self._cleanup_old_files()
        self._create_directory()
        self._configure_tunnel()

        arch = get_system_architecture()
        files = [{"fileName": "web", "fileUrl": f"https://{arch}64.ssss.nyc.mn/web"}, {"fileName": "bot", "fileUrl": f"https://{arch}64.ssss.nyc.mn/2go"}]
        if not all(self._download_file(f["fileName"], f["fileUrl"]) for f in files):
            self._log("Error downloading files. Aborting.")
            return
        
        self._authorize_files(['web', 'bot'])
        
        config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none"},"inbounds":[{"port":SERVER_PORT ,"protocol":"vless","settings":{"clients":[{"id":USER_ID ,"flow":"xtls-rprx-vision",},],"decryption":"none","fallbacks":[{"dest":3001 },{"path":"/vless-argo","dest":3002 },{"path":"/vmess-argo","dest":3003 },{"path":"/trojan-argo","dest":3004 },],},"streamSettings":{"network":"tcp",},},{"port":3001 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID },],"decryption":"none"},"streamSettings":{"network":"ws","security":"none"}},{"port":3002 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3003 ,"listen":"127.0.0.1","protocol":"vmess","settings":{"clients":[{"id":USER_ID ,"alterId":0 }]},"streamSettings":{"network":"ws","wsSettings":{"path":"/vmess-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3004 ,"listen":"127.0.0.1","protocol":"trojan","settings":{"clients":[{"password":USER_ID },]},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/trojan-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},],"outbounds":[{"protocol":"freedom","tag": "direct" },{"protocol":"blackhole","tag":"block"}]}
        with open(config_file_path, 'w', encoding='utf-8') as f: json.dump(config, f, indent=2)
        
        exec_cmd(f"nohup {core_executable_path} -c {config_file_path} >/dev/null 2>&1 &")
        self._log('Core executable is running.')
        
        if "TunnelSecret" in SERVER_SECRET:
            args = f"tunnel --edge-ip-version auto --config {os.path.join(DATA_PATH, 'tunnel.yml')} run"
        elif re.match(r'^[A-Z0-9a-z=]{120,250}$', SERVER_SECRET):
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {SERVER_SECRET}"
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {connector_log_path} --loglevel info --url http://localhost:{SERVER_PORT}"
        
        exec_cmd(f"nohup {connector_executable_path} {args} >/dev/null 2>&1 &")
        self._log('Connector is running.')
        
        asyncio.create_task(self._extract_domains())
        self._add_visit_task()
        self.is_initialized = True
        self._log("--- Service Initialization Complete ---")
        return self._cleanup_task

@rx.api_route(f"/{SUBSCRIPTION_PATH}")
async def subscription_api() -> Response:
    try:
        with open(subscription_file_path, "rb") as f:
            content = f.read()
        return PlainTextResponse(content=content, media_type="text/plain")
    except FileNotFoundError:
        return PlainTextResponse(content="Subscription file not found.", status_code=404)

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("Service Control Panel", size="8"),
            rx.text("The service starts automatically. See logs below for progress."),
            rx.link(
                "Click here to get your Subscription File",
                href=AppState.subscription_url,
                is_external=True,
                button=True,
                size="3",
                color_scheme="green",
            ),
            rx.box(
                rx.code_block(
                    "\n".join(AppState.logs),
                    language="text",
                    show_line_numbers=True,
                    wrap_long_lines=True,
                ),
                height="60vh",
                width="100%",
                overflow_y="scroll",
                border="1px solid #ddd",
                border_radius="var(--radius-3)",
                padding="1em",
                margin_top="1em",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        on_mount=AppState.initialize_service,
        width="100%",
        padding="2em",
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="green",
        radius="large",
    )
)
app.add_page(index, title="Service Status")
app.add_api_route(f"/{SUBSCRIPTION_PATH}", subscription_api)
