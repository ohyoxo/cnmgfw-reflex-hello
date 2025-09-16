import reflex as rx
from my_app.api import app as api_app

config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",
    api_url="http://0.0.0.0:8000",
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
    app_module="my_app.my_app",
    api_module="my_app.api:app",
)
