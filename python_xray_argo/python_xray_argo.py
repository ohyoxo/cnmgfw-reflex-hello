import reflex as rx
import os
import re
import json
import time
import base64
import shutil
import platform
import subprocess
import requests
from typing import List

# --- Environment Variables ---
# Load environment variables, providing default values.
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

class AppState(rx.State):
    """Manages the application state and core logic."""
    status: str = "Initializing..."
    log_messages: List[str] = []
    subscription_content: str = "Generating, please wait..."

    # --- File Paths ---
    @rx.var
    def core_executable_path(self) -> str:
        return os.path.join(DATA_PATH, 'web')

    @rx.var
    def connector_executable_path(self) -> str:
        return os.path.join(DATA_PATH, 'bot')

    @rx.var
    def subscription_file_path(self) -> str:
        return os.path.join(DATA_PATH, 'sub.txt')

    @rx.var
    def links_file_path(self) -> str:
        return os.path.join(DATA_PATH, 'list.txt')

    @rx.var
    def connector_log_path(self) -> str:
        return os.path.join(DATA_PATH, 'boot.log')

    @rx.var
    def config_file_path(self) -> str:
        return os.path.join(DATA_PATH, 'config.json')

    # --- Core Logic as Background Tasks ---
    async def start_services(self):
        """Event handler to start the setup process on page load."""
        yield self._add_log("Starting services...")
        return self._start_server_background

    @rx.background
    async def _start_server_background(self):
        """The main logic, running in the background."""
        async with self:
            try:
                self.status = "Setting up..."
                self._delete_nodes()
                self._cleanup_old_files()
                self._create_directory()
                self._configure_tunnel()
                await self._download_files_and_run()
                self._add_visit_task()
                self.status = "Running"
                self._add_log("Setup complete. The application is running.")
            except Exception as e:
                self.status = f"Error: {e}"
                self._add_log(f"An error occurred: {e}")

    # --- Helper Methods (ported from original script) ---
    def _add_log(self, message: str):
        self.log_messages.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    def _exec_cmd(self, command: str):
        self._add_log(f"Executing command: {command}")
        try:
            # Using Popen for non-blocking execution, especially for nohup
            subprocess.Popen(
                command, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        except Exception as e:
            self._add_log(f"Error executing command: {e}")

    def _get_system_architecture(self) -> str:
        architecture = platform.machine().lower()
        return 'arm' if 'arm' in architecture or 'aarch64' in architecture else 'amd'

    def _download_file(self, file_name: str, file_url: str) -> bool:
        file_path = os.path.join(DATA_PATH, file_name)
        try:
            self._add_log(f"Downloading {file_name} from {file_url}...")
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self._add_log(f"Download {file_name} successful.")
            return True
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            self._add_log(f"Download {file_name} failed: {e}")
            return False

    def _authorize_files(self, file_paths: List[str]):
        for relative_file_path in file_paths:
            absolute_file_path = os.path.join(DATA_PATH, relative_file_path)
            if os.path.exists(absolute_file_path):
                try:
                    os.chmod(absolute_file_path, 0o775)
                    self._add_log(f"Set execute permission for {absolute_file_path}")
                except Exception as e:
                    self._add_log(f"Failed to set permission for {absolute_file_path}: {e}")

    def _create_directory(self):
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            self._add_log(f"Created directory: {DATA_PATH}")
        else:
            self._add_log(f"Directory already exists: {DATA_PATH}")

    def _cleanup_old_files(self):
        paths_to_delete = ['web', 'bot', 'boot.log', 'list.txt']
        for item in paths_to_delete:
            path = os.path.join(DATA_PATH, item)
            try:
                if os.path.exists(path):
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                    self._add_log(f"Removed old file/directory: {path}")
            except Exception as e:
                self._add_log(f"Error removing {path}: {e}")

    def _delete_nodes(self):
        # This function interacts with an external webhook.
        pass # Implementation can be added if needed.

    def _configure_tunnel(self):
        if not SERVER_SECRET or not SERVER_DOMAIN:
            self._add_log("SERVER_DOMAIN or SERVER_SECRET is empty. Using quick tunnels.")
            return

        if "TunnelSecret" in SERVER_SECRET:
            # Logic to create tunnel.json and tunnel.yml
            pass # Implementation can be added if needed.
        else:
            self._add_log("Using token to connect to tunnel.")

    async def _download_files_and_run(self):
        architecture = self._get_system_architecture()
        self._add_log(f"System architecture detected: {architecture}")

        files_map = {
            'arm': [{"fileName": "web", "fileUrl": "https://arm64.ssss.nyc.mn/web"}, {"fileName": "bot", "fileUrl": "https://arm64.ssss.nyc.mn/2go"}],
            'amd': [{"fileName": "web", "fileUrl": "https://amd64.ssss.nyc.mn/web"}, {"fileName": "bot", "fileUrl": "https://amd64.ssss.nyc.mn/2go"}]
        }
        files_to_download = files_map.get(architecture, [])

        if not all(self._download_file(f["fileName"], f["fileUrl"]) for f in files_to_download):
            self.status = "Error: Failed to download necessary files."
            return

        self._authorize_files(['web', 'bot'])

        config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":SERVER_PORT ,"protocol":"vless","settings":{"clients":[{"id":USER_ID ,"flow":"xtls-rprx-vision",},],"decryption":"none","fallbacks":[{"dest":3001 },{"path":"/vless-argo","dest":3002 },{"path":"/vmess-argo","dest":3003 },{"path":"/trojan-argo","dest":3004 },],},"streamSettings":{"network":"tcp",},},{"port":3001 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID },],"decryption":"none"},"streamSettings":{"network":"ws","security":"none"}},{"port":3002 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3003 ,"listen":"127.0.0.1","protocol":"vmess","settings":{"clients":[{"id":USER_ID ,"alterId":0 }]},"streamSettings":{"network":"ws","wsSettings":{"path":"/vmess-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3004 ,"listen":"127.0.0.1","protocol":"trojan","settings":{"clients":[{"password":USER_ID },]},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/trojan-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},],"outbounds":[{"protocol":"freedom","tag": "direct" },{"protocol":"blackhole","tag":"block"}]}
        with open(self.config_file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        self._add_log(f"Generated config file at {self.config_file_path}")

        self._exec_cmd(f"nohup {self.core_executable_path} -c {self.config_file_path} >/dev/null 2>&1 &")
        time.sleep(1)

        if os.path.exists(self.connector_executable_path):
            if re.match(r'^[A-Z0-9a-z=]{120,250}$', SERVER_SECRET):
                args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {SERVER_SECRET}"
            elif "TunnelSecret" in SERVER_SECRET:
                args = f"tunnel --edge-ip-version auto --config {os.path.join(DATA_PATH, 'tunnel.yml')} run"
            else:
                args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {self.connector_log_path} --loglevel info --url http://localhost:{SERVER_PORT}"
            
            self._exec_cmd(f"nohup {self.connector_executable_path} {args} >/dev/null 2>&1 &")
            time.sleep(2)

        time.sleep(5)
        await self._extract_domains()

    async def _extract_domains(self):
        domain = SERVER_DOMAIN if SERVER_SECRET and SERVER_DOMAIN else None
        if not domain:
            try:
                # Wait for the log file to be created and populated
                for _ in range(10): # Try for 10 seconds
                    if os.path.exists(self.connector_log_path):
                        with open(self.connector_log_path, 'r') as f:
                            content = f.read()
                            match = re.search(r'https?://([^ ]*trycloudflare\.com)/?', content)
                            if match:
                                domain = match.group(1)
                                break
                    time.sleep(1)
            except Exception as e:
                self._add_log(f"Error reading connector log: {e}")
        
        if domain:
            self._add_log(f"Found server domain: {domain}")
            await self._generate_links(domain)
        else:
            self._add_log("Could not determine server domain.")
            self.status = "Error: Could not find server domain."

    async def _generate_links(self, server_domain: str):
        try:
            meta_info_proc = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
            meta_info = meta_info_proc.stdout.split('"')
            isp = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()
        except Exception:
            isp = "CF"

        vmess_payload = {"v": "2", "ps": f"{BOT_NAME}-{isp}", "add": ENDPOINT_IP, "port": ENDPOINT_PORT, "id": USER_ID, "aid": "0", "scy": "none", "net": "ws", "type": "none", "host": server_domain, "path": "/vmess-argo?ed=2560", "tls": "tls", "sni": server_domain, "alpn": "", "fp": "chrome"}
        vmess_json = json.dumps(vmess_payload)
        vmess_b64 = base64.b64encode(vmess_json.encode('utf-8')).decode('utf-8')

        links = f"""vless://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?encryption=none&security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Fvless-argo%3Fed%3D2560#{BOT_NAME}-{isp}\n\nvmess://{vmess_b64}\n\ntrojan://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?security=tls&sni={server_domain}&fp=chrome&type=ws&host={server_domain}&path=%2Ftrojan-argo%3Fed%3D2560#{BOT_NAME}-{isp}"""
        
        with open(self.links_file_path, 'w', encoding='utf-8') as f:
            f.write(links)

        sub_b64 = base64.b64encode(links.encode('utf-8')).decode('utf-8')
        self.subscription_content = sub_b64
        with open(self.subscription_file_path, 'w', encoding='utf-8') as f:
            f.write(sub_b64)
        
        self._add_log("Subscription links generated successfully.")
        self._send_telegram()
        # self._upload_nodes() # Can be enabled if needed

    def _send_telegram(self):
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            return
        try:
            message = f"Subscription updated for {BOT_NAME}:\n\n{self.subscription_content}"
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            requests.post(url, params=params)
            self._add_log("Sent notification to Telegram.")
        except Exception as e:
            self._add_log(f"Failed to send Telegram message: {e}")

    def _add_visit_task(self):
        if not ENABLE_KEEP_ALIVE or not APP_URL:
            return
        # Logic for keep-alive service
        pass

# --- API Route ---
async def get_subscription(state: AppState):
    """API endpoint to serve the subscription file."""
    if os.path.exists(state.subscription_file_path):
        with open(state.subscription_file_path, 'r') as f:
            content = f.read()
        return rx.text(content, media_type="text/plain")
    return rx.text("Subscription not generated yet.", status_code=404)

# --- Frontend UI ---
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Proxy Subscription Generator", size="7"),
            rx.box(
                "Status: ",
                rx.code(AppState.status),
                padding_y="1em",
            ),
            rx.text("Your subscription link content (Base64):"),
            rx.text_area(
                value=AppState.subscription_content,
                is_read_only=True,
                width="100%",
                height="200px",
                font_family="monospace",
            ),
            rx.button(
                "Copy to Clipboard",
                on_click=rx.set_clipboard(AppState.subscription_content),
                margin_top="1em",
            ),
            rx.accordion(
                rx.accordion_item(
                    rx.accordion_button(
                        rx.text("Logs"),
                        rx.accordion_icon(),
                    ),
                    rx.accordion_panel(
                        rx.box(
                            rx.foreach(
                                AppState.log_messages,
                                lambda msg: rx.text(msg, as_="p", font_family="monospace", font_size="0.8em")
                            ),
                            height="300px",
                            width="100%",
                            overflow_y="scroll",
                            border="1px solid #ddd",
                            padding="1em",
                            margin_top="1em",
                        )
                    ),
                ),
                width="100%",
            ),
            spacing="5",
            width="80%",
            max_width="800px",
        ),
        on_mount=AppState.start_services,
    )

# --- App Initialization ---
app = rx.App()
app.add_page(index)
app.api.add_api_route(f"/{SUBSCRIPTION_PATH}", get_subscription)
