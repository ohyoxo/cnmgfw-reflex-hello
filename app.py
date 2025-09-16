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
import threading
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

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
HTTP_PORT = int(os.environ.get('HTTP_PORT') or os.environ.get('PORT') or 3000)

# Create running folder
def create_directory():
    print('\033c', end='')
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"{DATA_PATH} is created")
    else:
        print(f"{DATA_PATH} already exists")

# Global variables
core_executable_path = os.path.join(DATA_PATH, 'web')
connector_executable_path = os.path.join(DATA_PATH, 'bot')
subscription_file_path = os.path.join(DATA_PATH, 'sub.txt')
links_file_path = os.path.join(DATA_PATH, 'list.txt')
connector_log_path = os.path.join(DATA_PATH, 'boot.log')
config_file_path = os.path.join(DATA_PATH, 'config.json')

# Delete nodes
def delete_nodes():
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

# Clean up old files
def cleanup_old_files():
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

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello World')
            
        elif self.path == f'/{SUBSCRIPTION_PATH}':
            try:
                with open(subscription_file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass
    
# Determine system architecture
def get_system_architecture():
    architecture = platform.machine().lower()
    if 'arm' in architecture or 'aarch64' in architecture:
        return 'arm'
    else:
        return 'amd'

# Download file based on architecture
def download_file(file_name, file_url):
    file_path = os.path.join(DATA_PATH, file_name)
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download {file_name} successfully")
        return True
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"Download {file_name} failed: {e}")
        return False

# Get files for architecture
def get_files_for_architecture(architecture):
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

# Authorize files with execute permission
def authorize_files(file_paths):
    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(DATA_PATH, relative_file_path)
        if os.path.exists(absolute_file_path):
            try:
                os.chmod(absolute_file_path, 0o775)
                print(f"Empowerment success for {absolute_file_path}: 775")
            except Exception as e:
                print(f"Empowerment failed for {absolute_file_path}: {e}")

# Configure server tunnel
def configure_tunnel():
    if not SERVER_SECRET or not SERVER_DOMAIN:
        print("SERVER_DOMAIN or SERVER_SECRET variable is empty, use quick tunnels")
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
    else:
        print("Use token connect to tunnel,please set the {SERVER_PORT} in cloudflare")

# Execute shell command and return output
def exec_cmd(command):
    try:
        process = subprocess.Popen(
            command, 
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return stdout + stderr
    except Exception as e:
        print(f"Error executing command: {e}")
        return str(e)

# Download and run necessary files
async def download_files_and_run():
    global private_key, public_key
    
    architecture = get_system_architecture()
    files_to_download = get_files_for_architecture(architecture)
    
    if not files_to_download:
        print("Can't find a file for the current architecture")
        return
    
    # Download all files
    download_success = True
    for file_info in files_to_download:
        if not download_file(file_info["fileName"], file_info["fileUrl"]):
            download_success = False
    
    if not download_success:
        print("Error downloading files")
        return
    
    # Authorize files
    files_to_authorize = ['web', 'bot']
    authorize_files(files_to_authorize)
    
    # Generate configuration file
    config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":SERVER_PORT ,"protocol":"vless","settings":{"clients":[{"id":USER_ID ,"flow":"xtls-rprx-vision",},],"decryption":"none","fallbacks":[{"dest":3001 },{"path":"/vless-argo","dest":3002 },{"path":"/vmess-argo","dest":3003 },{"path":"/trojan-argo","dest":3004 },],},"streamSettings":{"network":"tcp",},},{"port":3001 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID },],"decryption":"none"},"streamSettings":{"network":"ws","security":"none"}},{"port":3002 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":USER_ID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3003 ,"listen":"127.0.0.1","protocol":"vmess","settings":{"clients":[{"id":USER_ID ,"alterId":0 }]},"streamSettings":{"network":"ws","wsSettings":{"path":"/vmess-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3004 ,"listen":"127.0.0.1","protocol":"trojan","settings":{"clients":[{"password":USER_ID },]},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/trojan-argo"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},],"outbounds":[{"protocol":"freedom","tag": "direct" },{"protocol":"blackhole","tag":"block"}]}
    with open(config_file_path, 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)
    
    # Run core executable
    command = f"nohup {core_executable_path} -c {config_file_path} >/dev/null 2>&1 &"
    try:
        exec_cmd(command)
        print('Core executable is running')
        time.sleep(1)
    except Exception as e:
        print(f"web running error: {e}")
    
    # Run connector executable
    if os.path.exists(connector_executable_path):
        if re.match(r'^[A-Z0-9a-z=]{120,250}$', SERVER_SECRET):
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {SERVER_SECRET}"
        elif "TunnelSecret" in SERVER_SECRET:
            args = f"tunnel --edge-ip-version auto --config {os.path.join(DATA_PATH, 'tunnel.yml')} run"
        else:
            args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {connector_log_path} --loglevel info --url http://localhost:{SERVER_PORT}"
        
        try:
            exec_cmd(f"nohup {connector_executable_path} {args} >/dev/null 2>&1 &")
            print('Connector is running')
            time.sleep(2)
        except Exception as e:
            print(f"Error executing command: {e}")
    
    time.sleep(5)
    
    # Extract domains and generate sub.txt
    await extract_domains()

# Extract domains from connector logs
async def extract_domains():
    server_domain = None

    if SERVER_SECRET and SERVER_DOMAIN:
        server_domain = SERVER_DOMAIN
        print(f'SERVER_DOMAIN: {server_domain}')
        await generate_links(server_domain)
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
                print(f'ServerDomain: {server_domain}')
                await generate_links(server_domain)
            else:
                print('ServerDomain not found, re-running connector to obtain ServerDomain')
                if os.path.exists(connector_log_path):
                    os.remove(connector_log_path)
                
                try:
                    exec_cmd('pkill -f "[b]ot" > /dev/null 2>&1')
                except:
                    pass
                
                time.sleep(1)
                args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {DATA_PATH}/boot.log --loglevel info --url http://localhost:{SERVER_PORT}'
                exec_cmd(f'nohup {connector_executable_path} {args} >/dev/null 2>&1 &')
                print('Connector is running.')
                time.sleep(6)
                await extract_domains()
        except Exception as e:
            print(f'Error reading connector log: {e}')

# Upload nodes to subscription service
def upload_nodes():
    if WEBHOOK_URL and APP_URL:
        subscription_url = f"{APP_URL}/{SUBSCRIPTION_PATH}"
        json_data = {
            "subscription": [subscription_url]
        }
        
        try:
            response = requests.post(
                f"{WEBHOOK_URL}/api/add-subscriptions",
                json=json_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print('Subscription uploaded successfully')
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
            response = requests.post(
                f"{WEBHOOK_URL}/api/add-nodes",
                data=json_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print('Nodes uploaded successfully')
        except:
            return None
    else:
        return
    
# Send notification to Telegram
def send_telegram():
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
        print('Telegram message sent successfully')
    except Exception as e:
        print(f'Failed to send Telegram message: {e}')

# Generate links and subscription content
async def generate_links(server_domain):
    meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
    meta_info = meta_info.stdout.split('"')
    ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()

    time.sleep(2)
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
        
    print(sub_txt)
    
    print(f"{DATA_PATH}/sub.txt saved successfully")
    
    # Additional actions
    send_telegram()
    upload_nodes()
  
    return sub_txt   
 
# Add automatic access task
def add_visit_task():
    if not ENABLE_KEEP_ALIVE or not APP_URL:
        print("Skipping adding automatic access task")
        return
    
    try:
        response = requests.post(
            'https://keep.gvrander.eu.org/add-url',
            json={"url": APP_URL},
            headers={"Content-Type": "application/json"}
        )
        print('automatic access task added successfully')
    except Exception as e:
        print(f'Failed to add URL: {e}')

# Clean up files after 90 seconds
def clean_files():
    def _cleanup():
        time.sleep(90)
        files_to_delete = [connector_log_path, config_file_path, links_file_path, core_executable_path, connector_executable_path]
        
        for file in files_to_delete:
            try:
                if os.path.exists(file):
                    if os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
            except:
                pass
        
        print('\033c', end='')
        print('App is running')
        print('Thank you for using this script, enjoy!')
    
    threading.Thread(target=_cleanup, daemon=True).start()
    
# Main function to start the server
async def start_server():
    delete_nodes()
    cleanup_old_files()
    create_directory()
    configure_tunnel()
    await download_files_and_run()
    add_visit_task()
    
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()   
    
    clean_files()
    
def run_server():
    server = HTTPServer(('0.0.0.0', HTTP_PORT), RequestHandler)
    print(f"Server is running on port {HTTP_PORT}")
    print(f"Running done！")
    print(f"\nLogs will be delete in 90 seconds")
    server.serve_forever()
    
def run_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server()) 
    
    while True:
        time.sleep(3600)
        
if __name__ == "__main__":
    run_async()
