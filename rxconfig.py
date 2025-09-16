import reflex as rx

config = rx.Config(
    app_name="my_app",
    db_url="sqlite:///reflex.db",
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
)
