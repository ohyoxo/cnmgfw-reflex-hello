# rxconfig.py
import reflex as rx

# 配置应用
config = rx.Config(
    app_name="hello",
    api_url="http://localhost:8000",
    frontend_port=3000,
    backend_port=8000,
)
