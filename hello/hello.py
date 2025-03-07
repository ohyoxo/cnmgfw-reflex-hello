import reflex as rx
from hello.utils import run_server_in_background, visit_project_page, FILE_PATH, INTERVAL_SECONDS
import os

class State(rx.State):
    sub_content: str = ""
    status: str = "Initializing..."

    def load_sub_content(self):
        try:
            with open(os.path.join(FILE_PATH, 'sub.txt'), 'rb') as file:
                self.sub_content = file.read().decode('utf-8')
            self.status = "App is running"
        except FileNotFoundError:
            self.sub_content = "sub.txt not found"
            self.status = "Error loading sub content"

    async def periodic_visit(self):
        while True:
            visit_project_page()
            await rx.sleep(INTERVAL_SECONDS)

def index():
    return rx.vstack(
        rx.text(State.status, font_size="24px"),
        rx.cond(
            State.sub_content,
            rx.text_area(value=State.sub_content, is_read_only=True, width="100%", height="300px"),
            rx.text("Loading subscription content...")
        ),
        on_mount=[State.load_sub_content, State.periodic_visit],
        padding="20px",
        width="100%",
    )

app = rx.App(state=State)
app.add_page(index, route="/")
app.add_page(lambda: rx.text("Hello, world"), route="/hello")
app.add_page(lambda: rx.text(State.sub_content) if State.sub_content else rx.text("Error reading file"), route="/sub")

# Start server in background
run_server_in_background()
