import reflex as rx

config = rx.Config(
    app_name="hello",
    api_url="http://localhost:8000",
    db_url="sqlite:///reflex.db",
    frontend_port=3000,  # 与原始项目 PORT 对应
    backend_port=8000,
)
