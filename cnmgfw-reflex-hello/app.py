# my_reflex_app/app.py
import reflex as rx
from my_reflex_app.state import State
import os

# Styling
container_style = dict(
    width="100%",
    padding="20px",
    max_width="800px",
    margin="0 auto",
)

status_style = dict(
    padding="10px",
    border_radius="5px",
    background_color=rx.color("gray", 2),
    margin_bottom="10px",
)

button_style = dict(
    padding="10px 20px",
    background_color=rx.color("accent", 8),
    color="white",
    border_radius="5px",
    cursor="pointer",
)

# Components
def status_display() -> rx.Component:
    return rx.box(
        rx.text("Status: ", State.status),
        rx.text("Sub Content: ", rx.cond(
            State.sub_content,
            State.sub_content,
            "Not generated yet"
        )),
        style=status_style,
    )

def control_buttons() -> rx.Component:
    return rx.hstack(
        rx.button(
            "Start Server",
            on_click=State.start_server,
            style=button_style,
        ),
        rx.button(
            "Visit Project Page",
            on_click=State.visit_project_page,
            style=button_style,
        ),
        spacing="4",
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("VLESS Configuration Server", size="8"),
            status_display(),
            control_buttons(),
            align="center",
            spacing="6",
        ),
        style=container_style,
    )

# Create and configure the app
app = rx.App()
app.add_page(index, title="VLESS Server Manager")
