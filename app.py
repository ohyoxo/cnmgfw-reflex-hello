import reflex as rx
import base64
import json
import os

# 从环境变量获取配置，如果不存在则使用默认值
USER_ID = os.environ.get('USER_ID', 'ae1ea14e-5fc1-470a-bd0f-f1365c1ebc89')
ENDPOINT_IP = os.environ.get('ENDPOINT_IP', 'cf.877774.xyz')
ENDPOINT_PORT = os.environ.get('ENDPOINT_PORT', '443')
BOT_NAME = os.environ.get('BOT_NAME', 'Reflex-Proxy')
ISP_INFO = os.environ.get('ISP_INFO', 'Cloudflare-US')

class State(rx.State):
    """应用的状态管理"""
    server_domain: str = "your-server-domain.com"  # 默认或从环境变量获取
    subscription_content: str = ""
    
    def generate_links(self):
        """生成订阅链接"""
        if not self.server_domain or self.server_domain == "your-server-domain.com":
            # 可以在这里添加一个提示，让用户输入域名
            return

        vmess_config = {
            "v": "2", 
            "ps": f"{BOT_NAME}-{ISP_INFO}", 
            "add": ENDPOINT_IP, 
            "port": ENDPOINT_PORT, 
            "id": USER_ID, 
            "aid": "0", 
            "scy": "none", 
            "net": "ws", 
            "type": "none", 
            "host": self.server_domain, 
            "path": "/vmess-argo?ed=2560", 
            "tls": "tls", 
            "sni": self.server_domain, 
            "alpn": "", 
            "fp": "chrome"
        }
        
        vmess_link = "vmess://" + base64.b64encode(json.dumps(vmess_config).encode('utf-8')).decode('utf-8')
        
        vless_link = f"vless://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?encryption=none&security=tls&sni={self.server_domain}&fp=chrome&type=ws&host={self.server_domain}&path=%2Fvless-argo%3Fed%3D2560#{BOT_NAME}-{ISP_INFO}"
        
        trojan_link = f"trojan://{USER_ID}@{ENDPOINT_IP}:{ENDPOINT_PORT}?security=tls&sni={self.server_domain}&fp=chrome&type=ws&host={self.server_domain}&path=%2Ftrojan-argo%3Fed%3D2560#{BOT_NAME}-{ISP_INFO}"

        links_text = f"{vless_link}\n\n{vmess_link}\n\n{trojan_link}"
        
        self.subscription_content = base64.b64encode(links_text.encode('utf-8')).decode('utf-8')

def index():
    """主页面"""
    return rx.center(
        rx.vstack(
            rx.heading("代理订阅链接生成器", size="9"),
            rx.text("输入你的服务器域名，然后点击生成按钮。"),
            
            rx.input(
                placeholder="例如: my.domain.com",
                on_blur=State.set_server_domain,
                width="400px"
            ),
            
            rx.button("生成订阅链接", on_click=State.generate_links, margin_top="1rem"),
            
            rx.cond(
                State.subscription_content,
                rx.box(
                    rx.heading("订阅内容 (Base64编码)", size="5", margin_top="2rem"),
                    rx.code_block(
                        State.subscription_content,
                        language="text",
                        can_copy=True,
                        width="600px",
                        max_height="200px"
                    ),
                    rx.text("将以上内容复制到你的代理客户端中。")
                )
            ),
            
            spacing="5",
            align="center",
            padding="2rem"
        ),
        width="100%",
        height="100vh"
    )

# 创建并配置应用
app = rx.App()
app.add_page(index)
