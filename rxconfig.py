import reflex as rx

config = rx.Config(
    app_name="myapps",  # <-- 在这里修改你的应用名！
    # 部署后的网址将是 your-app-name.reflex.run
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
)

