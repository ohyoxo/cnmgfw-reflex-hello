import reflex as rx

config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",
    api_url="http://0.0.0.0:8000",
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
)
