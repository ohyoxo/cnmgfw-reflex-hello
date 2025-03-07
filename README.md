Introduction
Reflex is an open-source framework for quickly building beautiful, interactive web applications in pure Python.

Goals
Pure Python

Use Python for everything. Don't worry about learning a new language.

Easy to Learn

Build and share your first app in minutes. No web development experience required.

Full Flexibility

Remain as flexible as traditional web frameworks. Reflex is easy to use, yet allows for advanced use cases.

Build anything from small data science apps to large, multi-page websites. This entire site was built and deployed with Reflex!

Batteries Included

No need to reach for a bunch of different tools. Reflex handles the user interface, server-side logic, and deployment of your app.

An example: Make it count
Here, we go over a simple counter app that lets the user count up or down.

Decrement
0
Increment
Here is the full code for this example:

Frontend
Backend
Page
Write your backend in the State class. Here you can define functions and variables that can be referenced in the frontend. This code runs directly on the server and is not compiled, so there are no special caveats. Here you can use any Python external library and call any method/function.

import reflex as rx 
class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1
def index():
    return rx.hstack(
        rx.button(
            "Decrement",
            color_scheme="ruby",
            on_click=State.decrement,
        ),
        rx.heading(State.count, font_size="2em"),
        rx.button(
            "Increment",
            color_scheme="grass",
            on_click=State.increment,
        ),
        spacing="4",
    )
app = rx.App()
app.add_page(index)
The Structure of a Reflex App
Let's break this example down.

Import
import reflex as rx

We begin by importing the reflex package (aliased to rx). We reference Reflex objects as rx.* by convention.

State
class State(rx.State):
    count: int = 0

The state defines all the variables (called vars) in an app that can change, as well as the functions (called event_handlers) that change them.

Here our state has a single var, count, which holds the current value of the counter. We initialize it to 0.

Event Handlers
def increment(self):
    self.count += 1


def decrement(self):
    self.count -= 1

Within the state, we define functions, called event handlers, that change the state vars.

Event handlers are the only way that we can modify the state in Reflex. They can be called in response to user actions, such as clicking a button or typing in a text box. These actions are called events.

Our counter app has two event handlers, increment and decrement.

User Interface (UI)
def index():
    return rx.hstack(
        rx.button(
            "Decrement",
            color_scheme="ruby",
            on_click=State.decrement,
        ),
        rx.heading(State.count, font_size="2em"),
        rx.button(
            "Increment",
            color_scheme="grass",
            on_click=State.increment,
        ),
        spacing="4",
    )

This function defines the app's user interface.

We use different components such as rx.hstack, rx.button, and rx.heading to build the frontend. Components can be nested to create complex layouts, and can be styled using the full power of CSS.

Reflex comes with 50+ built-in components to help you get started. We are actively adding more components. Also, it's easy to wrap your own React components.

rx.heading(State.count, font_size="2em"),

Components can reference the app's state vars. The rx.heading component displays the current value of the counter by referencing State.count. All components that reference state will reactively update whenever the state changes.

rx.button(
    "Decrement",
    color_scheme="ruby",
    on_click=State.decrement,
),

Components interact with the state by binding events triggers to event handlers. For example, on_click is an event that is triggered when a user clicks a component.

The first button in our app binds its on_click event to the State.decrement event handler. Similarly the second button binds on_click to State.increment.

In other words, the sequence goes like this:

User clicks "increment" on the UI.
on_click event is triggered.
Event handler State.increment is called.
State.count is incremented.
UI updates to reflect the new value of State.count.
Add pages
Next we define our app and add the counter component to the base route.

app = rx.App()
app.add_page(index)

Next Steps
🎉 And that's it!

We've created a simple, yet fully interactive web app in pure Python.


Installation
Reflex requires Python 3.8+.


Video: Installation

Virtual Environment
We highly recommend creating a virtual environment for your project.

venv is the standard option. conda and poetry are some alternatives.

Install Reflex on your system
macOS/Linux
Windows
Install on macOS/Linux
We will go with venv here.

Prerequisites
macOS (Apple Silicon) users should install Rosetta 2. Run this command:

/usr/sbin/softwareupdate --install-rosetta --agree-to-license

Create the project directory
Replace my_app_name with your project name. Switch to the new directory.

mkdir my_app_name
cd my_app_name

Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate


Getting No module named venv?

Install Reflex package
Reflex is available as a pip package.

pip install reflex


Getting command not found: pip?

Initialize the project
reflex init


Error command not found: reflex Mac / Linux

The command will return four template options to choose from as shown below.

Initializing the web directory.

Get started with a template:
(0) blank (https://blank-template.reflex.run) - A minimal template
(1) dashboard (https://dashboard-new.reflex.run/) - A dashboard with tables and graphs
(2) sales (https://sales-new.reflex.run/) - An app to manage sales and customers
(3) ai_image_gen (https://ai-image-gen.reflex.run/) - An app to generate images using AI
(4) ci_template (https://cijob.reflex.run/) - A template for continuous integration
(5) api_admin_panel (https://api-admin-panel.reflex.run/) - An admin panel for an api.
(6) nba (https://nba-new.reflex.run/) - A data visualization app for NBA data.
(7) customer_data_app (https://customer-data-app.reflex.run/) - An app to manage customer data.
Which template would you like to use? (0): 

From here select a template.

Run the App
Run it in development mode:

reflex run

Your app runs at http://localhost:3000.

Reflex prints logs to the terminal. To increase log verbosity to help with debugging, use the --loglevel flag:

reflex run --loglevel debug

Reflex will hot reload any code changes in real time when running in development mode. Your code edits will show up on http://localhost:3000 automatically.

Reflex Basics
This page gives an introduction to the most common concepts that you will use to build Reflex apps.

You will learn how to:

Create and nest components
Customize and style components
Distinguish between compile-time and runtime
Display data that changes over time
Respond to events and update the screen
Render conditions and lists
Create pages and navigate between them
Install reflex using pip.

pip install reflex

Import the reflex library to get started.

import reflex as rx

Creating and nesting components
Components are the building blocks for your app's user interface (UI). They are the visual elements that make up your app, like buttons, text, and images. Reflex has a wide selection of built-in components to get you started quickly.

Components are created using functions that return a component object.

Click Me
def my_button():
    return rx.button("Click Me")

Components can be nested inside each other to create complex UIs.

To nest components as children, pass them as positional arguments to the parent component. In the example below, the rx.text and my_button components are children of the rx.box component.

This is a page

Click Me
def my_page():
    return rx.box(
        rx.text("This is a page"),
        # Reference components defined in other functions.
        my_button(),
    )

You can also use any base HTML element through the rx.el namespace.

Use base html!

def my_div():
    return rx.el.div(
        rx.el.p("Use base html!"),
    )

If you need a component not provided by Reflex, you can check the 3rd party ecosystem or wrap your own React component.

Customizing and styling components
Components can be customized using props, which are passed in as keyword arguments to the component function.

Each component has props that are specific to that component. Check the docs for the component you are using to see what props are available.

def half_filled_progress():
    return rx.progress(value=50)

In addition to component-specific props, components can also be styled using CSS properties passed as props.

Click Me
def round_button():
    return rx.button(
        "Click Me", border_radius="15px", font_size="18px"
    )


Use the snake_case version of the CSS property name as the prop name.

See the styling guide for more information on how to style components

In summary, components are made up of children and props.

Children
- Text or other Reflex components nested inside a component. - Passed as **positional arguments**.
Props
- Attributes that affect the behavior and appearance of a component. - Passed as **keyword arguments**.
Displaying data that changes over time
Apps need to store and display data that changes over time. Reflex handles this through State, which is a Python class that stores variables that can change when the app is running, as well as the functions that can change those variables.

To define a state class, subclass rx.State and define fields that store the state of your app. The state variables (vars) should have a type annotation, and can be initialized with a default value.

class MyState(rx.State):
    count: int = 0

Referencing state vars in components
To reference a state var in a component, you can pass it as a child or prop. The component will automatically update when the state changes.

Vars are referenced through class attributes on your state class. For example, to reference the count var in a component, use MyState.count.

Count:
0
class MyState(rx.State):
    count: int = 0
    color: str = "red"


def counter():
    return rx.hstack(
        # The heading `color` prop is set to the `color` var in MyState.
        rx.heading("Count: ", color=MyState.color),
        # The `count` var in `MyState` is passed as a child to the heading component.
        rx.heading(MyState.count),
    )

Vars can be referenced in multiple components, and will automatically update when the state changes.

Responding to events and updating the screen
So far, we've defined state vars but we haven't shown how to change them. All state changes are handled through functions in the state class, called event handlers.


Event handlers are the ONLY way to change state in Reflex.

Components have special props, such as on_click, called event triggers that can be used to make components interactive. Event triggers connect components to event handlers, which update the state.

0
Increment
class CounterState(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count += 1


def counter_increment():
    return rx.hstack(
        rx.heading(CounterState.count),
        rx.button(
            "Increment", on_click=CounterState.increment
        ),
    )

When an event trigger is activated, the event handler is called, which updates the state. The UI is automatically re-rendered to reflect the new state.


What is the @rx.event decorator?

Event handlers with arguments
Event handlers can also take in arguments. For example, the increment event handler can take an argument to increment the count by a specific amount.

0
Increment by 1
Increment by 5
class CounterState2(rx.State):
    count: int = 0

    @rx.event
    def increment(self, amount: int):
        self.count += amount


def counter_variable():
    return rx.hstack(
        rx.heading(CounterState2.count),
        rx.button(
            "Increment by 1",
            on_click=lambda: CounterState2.increment(1),
        ),
        rx.button(
            "Increment by 5",
            on_click=lambda: CounterState2.increment(5),
        ),
    )

The on_click event trigger doesn't pass any arguments here, but some event triggers do. For example, the on_blur event trigger passes the text of an input as an argument to the event handler.


class TextState(rx.State):
    text: str = ""

    @rx.event
    def update_text(self, new_text: str):
        self.text = new_text


def text_input():
    return rx.vstack(
        rx.heading(TextState.text),
        rx.input(
            default_value=TextState.text,
            on_blur=TextState.update_text,
        ),
    )


Make sure that the event handler has the same number of arguments as the event trigger, or an error will be raised.

Compile-time vs. runtime (IMPORTANT)
Before we dive deeper into state, it's important to understand the difference between compile-time and runtime in Reflex.

When you run your app, the frontend gets compiled to Javascript code that runs in the browser (compile-time). The backend stays in Python and runs on the server during the lifetime of the app (runtime).

When can you not use pure Python?
We cannot compile arbitrary Python code, only the components that you define. What this means importantly is that you cannot use arbitrary Python operations and functions on state vars in components.

However, since any event handlers in your state are on the backend, you can use any Python code or library within your state.

Examples that work
Within an event handler, use any Python code or library.

even
Increment
def check_even(num: int):
    return num % 2 == 0


class MyState3(rx.State):
    count: int = 0
    text: str = "even"

    @rx.event
    def increment(self):
        # Use any Python code within state.
        # Even reference functions defined outside the state.
        if check_even(self.count):
            self.text = "even"
        else:
            self.text = "odd"
        self.count += 1


def count_and_check():
    return rx.box(
        rx.heading(MyState3.text),
        rx.button("Increment", on_click=MyState3.increment),
    )

Use any Python function within components, as long as it is defined at compile time (i.e. does not reference any state var)

0true
1false
2true
3false
4true
5false
6true
7false
8true
9false
def show_numbers():
    return rx.vstack(
        *[rx.hstack(i, check_even(i)) for i in range(10)]
    )

Examples that don't work
You cannot do an if statement on vars in components, since the value is not known at compile time.

class BadState(rx.State):
    count: int = 0


def count_if_even():
    return rx.box(
        rx.heading("Count: "),
        # This will raise a compile error, as BadState.count is a var and not known at compile time.
        rx.text(
            BadState.count
            if BadState.count % 2 == 0
            else "Odd"
        ),
        # Using an if statement with a var as a prop will NOT work either.
        rx.text(
            "hello",
            color="red"
            if BadState.count % 2 == 0
            else "blue",
        ),
    )

You cannot do a for loop over a list of vars.

class BadState(rx.State):
    items: list[str] = ["Apple", "Banana", "Cherry"]


def loop_over_list():
    return rx.box(
        # This will raise a compile error, as BadState.items is a list and not known at compile time.
        *[rx.text(item) for item in BadState.items]
    )

You cannot do arbitrary Python operations on state vars in components.

class BadTextState(rx.State):
    text: str = "Hello world"


def format_text():
    return rx.box(
        # Python operations such as `len` will not work on state vars.
        rx.text(len(BadTextState.text)),
    )

In the next sections, we will show how to handle these cases.

Conditional rendering
As mentioned above, you cannot use Python if/else statements with state vars in components. Instead, use the rx.cond function to conditionally render components.

Not Logged In
Toggle Login
class LoginState(rx.State):
    logged_in: bool = False

    @rx.event
    def toggle_login(self):
        self.logged_in = not self.logged_in


def show_login():
    return rx.box(
        rx.cond(
            LoginState.logged_in,
            rx.heading("Logged In"),
            rx.heading("Not Logged In"),
        ),
        rx.button(
            "Toggle Login", on_click=LoginState.toggle_login
        ),
    )

Rendering lists
To iterate over a var that is a list, use the rx.foreach function to render a list of components.

Pass the list var and a function that returns a component as arguments to rx.foreach.

Apple
Banana
Cherry
class ListState(rx.State):
    items: list[str] = ["Apple", "Banana", "Cherry"]


def render_item(item: rx.Var[str]):
    """Render a single item."""
    # Note that item here is a Var, not a str!
    return rx.list.item(item)


def show_fruits():
    return rx.box(
        rx.foreach(ListState.items, render_item),
    )

The function that renders each item takes in a Var, since this will get compiled up front.

Var Operations
You can't use arbitrary Python operations on state vars in components, but Reflex has var operations that you can use to manipulate state vars.

For example, to check if a var is even, you can use the % and == var operations.

Count:
Even

Increment
class CountEvenState(rx.State):
    count: int = 0

    @rx.event
    def increment(self):
        self.count += 1


def count_if_even():
    return rx.box(
        rx.heading("Count: "),
        rx.cond(
            # Here we use the `%` and `==` var operations to check if the count is even.
            CountEvenState.count % 2 == 0,
            rx.text("Even"),
            rx.text("Odd"),
        ),
        rx.button(
            "Increment", on_click=CountEvenState.increment
        ),
    )

App and Pages
Reflex apps are created by instantiating the rx.App class. Pages are linked to specific URL routes, and are created by defining a function that returns a component.

def index():
    return rx.text("Root Page")


rx.app = rx.App()
app.add_page(index, route="/")

Next Steps
Now that you have a basic understanding of how Reflex works, the next step is to start coding your own apps. Try one of the following tutorials:

Project Structure
Directory Structure
Let's create a new app called hello

mkdir hello
cd hello
reflex init

This will create a directory structure like this:

hello
├── .web
├── assets
├── hello
│   ├── __init__.py
│   └── hello.py
└── rxconfig.py

Let's go over each of these directories and files.

.web
This is where the compiled Javascript files will be stored. You will never need to touch this directory, but it can be useful for debugging.

Each Reflex page will compile to a corresponding .js file in the .web/pages directory.

Assets
The assets directory is where you can store any static assets you want to be publicly available. This includes images, fonts, and other files.

For example, if you save an image to assets/image.png you can display it from your app like this:

rx.image(src="image.png")

Main Project
Initializing your project creates a directory with the same name as your app. This is where you will write your app's logic.

Reflex generates a default app within the hello/hello.py file. You can modify this file to customize your app.

Configuration
The rxconfig.py file can be used to configure your app. By default it looks something like this:

import reflex as rx


config = rx.Config(
    app_name="hello",
)

We will discuss project structure and configuration in more detail in the advanced project structure documentation.

Tutorial: Data Dashboard
During this tutorial you will build a small data dashboard, where you can input data and it will be rendered in table and a graph. This tutorial does not assume any existing Reflex knowledge, but we do recommend checking out the quick Basics Guide first.

The techniques you’ll learn in the tutorial are fundamental to building any Reflex app, and fully understanding it will give you a deep understanding of Reflex.

This tutorial is divided into several sections:

Setup for the Tutorial: A starting point to follow the tutorial
Overview: The fundamentals of Reflex UI (components and props)
Showing Dynamic Data: How to use State to render data that will change in your app.
Add Data to your App: Using a Form to let a user add data to your app and introduce event handlers.
Plotting Data in a Graph: How to use Reflex's graphing components.
Final Cleanup and Conclusion: How to further customize your app and add some extra styling to it.
What are you building?
In this tutorial, you are building an interactive data dashboard with Reflex.

You can see what the finished app and code will look like here:


Add User

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
Male
Female
0
0.25
0.5
0.75
1
import reflex as rx
from collections import Counter

class User(rx.Base):
    """The user model."""

    name: str
    email: str
    gender: str


class State(rx.State):
    users: list[User] = [
        User(name="Danilo Sousa", email="danilo@example.com", gender="Male"),
        User(name="Zahra Ambessa", email="zahra@example.com", gender="Female"),
    ]
    users_for_graph: list[dict] = []

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))
        self.transform_data()
    
    def transform_data(self):
        """Transform user gender group data into a format suitable for visualization in graphs."""
        # Count users of each gender group
        gender_counts = Counter(user.gender for user in self.users)
        
        # Transform into list of dict so it can be used in the graph
        self.users_for_graph = [
            {
                "name": gender_group,
                "value": count
            }
            for gender_group, count in gender_counts.items()
        ]
        

def show_user(user: User):
    """Show a user in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        style=\{"_hover": 
            {"bg": rx.color("gray", 3)}
        },
        align="center",
    )

def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add New User",
            ),
            rx.dialog.description(
                "Fill the form with the user's info",
            ),
            rx.form(
                rx.flex(
                    rx.input(
                        placeholder="User Name", name="name", required=True
                    ),
                    rx.input(
                        placeholder="user@reflex.dev",
                        name="email",
                    ),
                    rx.select(
                        ["Male", "Female"],
                        placeholder="male",
                        name="gender",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Submit", type="submit"
                            ),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )

def graph():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=State.users_for_graph,
        width="100%",
        height=250,
    )

def index() -> rx.Component:
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    State.users, show_user
                ),
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        graph(),
        align="center",
        width="100%",
    )


app = rx.App(
    theme=rx.theme(
        radius="full", accent_color="grass"
    ),
)

app.add_page(
    index,
    title="Customer Data App",
    description="A simple app to manage customer data.",
    on_load=State.transform_data,
)

Don't worry if you don't understand the code above, in this tutorial we are going to walk you through the whole thing step by step.

Setup for the tutorial
Check out the installation docs to get Reflex set up on your machine. Follow these to create a folder called dashboard_tutorial, which you will cd into and pip install reflex.

We will choose template 0 when we run reflex init to get the blank template. Finally run reflex run to start the app and confirm everything is set up correctly.

Overview
Now that you’re set up, let’s get an overview of Reflex!

Inspecting the starter code
Within our dashboard_tutorial folder we just cd'd into, there is a rxconfig.py file that contains the configuration for our Reflex app. (Check out the config docs for more information)

There is also an assets folder where static files such as images and stylesheets can be placed to be referenced within your app. (asset docs for more information)

Most importantly there is a folder also called dashboard_tutorial which contains all the code for your app. Inside of this folder there is a file named dashboard_tutorial.py. To begin this tutorial we will delete all the code in this file so that we can start from scratch and explain every step as we go.

The first thing we need to do is import reflex. Once we have done this we can create a component, which is a reusable piece of user interface code. Components are used to render, manage, and update the UI elements in your application.

Let's look at the example below. Here we have a function called index that returns a text component (an in-built Reflex UI component) that displays the text "Hello World!".

Next we define our app using app = rx.App() and add the component we just defined (index) to a page using app.add_page(index). The function name (in this example index) which defines the component, must be what we pass into the add_page. The definition of the app and adding a component to a page are required for every Reflex app.

import reflex as rx


def index() -> rx.Component:
    return rx.text("Hello World!")


app = rx.App()
app.add_page(index)

This code will render a page with the text "Hello World!" when you run your app like below:

Hello World!


For the rest of the tutorial the app=rx.App() and app.add_page will be implied and not shown in the code snippets.

Creating a table
Let's create a new component that will render a table. We will use the table component to do this. The table component has a root, which takes in a header and a body, which in turn take in row components. The row component takes in cell components which are the actual data that will be displayed in the table.

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
def index() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Gender"),
            ),
        ),
        rx.table.body(
            rx.table.row(
                rx.table.cell("Danilo Sousa"),
                rx.table.cell("danilo@example.com"),
                rx.table.cell("Male"),
            ),
            rx.table.row(
                rx.table.cell("Zahra Ambessa"),
                rx.table.cell("zahra@example.com"),
                rx.table.cell("Female"),
            ),
        ),
    )

Components in Reflex have props, which can be used to customize the component and are passed in as keyword arguments to the component function.

The rx.table.root component has for example the variant and size props, which customize the table as seen below.

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
def index() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Gender"),
            ),
        ),
        rx.table.body(
            rx.table.row(
                rx.table.cell("Danilo Sousa"),
                rx.table.cell("danilo@example.com"),
                rx.table.cell("Male"),
            ),
            rx.table.row(
                rx.table.cell("Zahra Ambessa"),
                rx.table.cell("zahra@example.com"),
                rx.table.cell("Female"),
            ),
        ),
        variant="surface",
        size="3",
    )

Showing dynamic data (State)
Up until this point all the data we are showing in the app is static. This is not very useful for a data dashboard. We need to be able to show dynamic data that can be added to and updated.

This is where State comes in. State is a Python class that stores variables that can change when the app is running, as well as the functions that can change those variables.

To define a state class, subclass rx.State and define fields that store the state of your app. The state variables (vars) should have a type annotation, and can be initialized with a default value. Check out the basics section for a simple example of how state works.

In the example below we define a State class called State that has a variable called users that is a list of lists of strings. Each list in the users list represents a user and contains their name, email and gender.

class State(rx.State):
    users: list[list[str]] = [
        ["Danilo Sousa", "danilo@example.com", "Male"],
        ["Zahra Ambessa", "zahra@example.com", "Female"],
    ]

To iterate over a state var that is a list, we use the rx.foreach function to render a list of components. The rx.foreach component takes an iterable (list, tuple or dict) and a function that renders each item in the iterable.


Why can we not just splat this in a for loop

Here the render function is show_user which takes in a single user and returns a table.row component that displays the users name, email and gender.

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
class State(rx.State):
    users: list[list[str]] = [
        ["Danilo Sousa", "danilo@example.com", "Male"],
        ["Zahra Ambessa", "zahra@example.com", "Female"],
    ]


def show_user(person: list):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(person[0]),
        rx.table.cell(person[1]),
        rx.table.cell(person[2]),
    )


def index() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Gender"),
            ),
        ),
        rx.table.body(
            rx.foreach(State.users, show_user),
        ),
        variant="surface",
        size="3",
    )

As you can see the output above looks the same as before, except now the data is no longer static and can change with user input to the app.

Using a proper class structure for our data
So far our data has been defined in a list of lists, where the data is accessed by index i.e. user[0], user[1]. This is not very maintainable as our app gets bigger.

A better way to structure our data in Reflex is to use a class to represent a user. This way we can access the data using attributes i.e. user.name, user.email.

In Reflex when we create these classes to showcase our data, the class must inherit from rx.Base.

rx.Base is also necessary if we want to have a state var that is an iterable with different types. For example if we wanted to have age as an int we would have to use rx.base as we could not do this with a state var defined as list[list[str]].

The show_user render function is also updated to access the data by named attributes, instead of indexing.

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
class User(rx.Base):
    """The user model."""

    name: str
    email: str
    gender: str


class State(rx.State):
    users: list[User] = [
        User(
            name="Danilo Sousa",
            email="danilo@example.com",
            gender="Male",
        ),
        User(
            name="Zahra Ambessa",
            email="zahra@example.com",
            gender="Female",
        ),
    ]


def show_user(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
    )


def index() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Name"),
                rx.table.column_header_cell("Email"),
                rx.table.column_header_cell("Gender"),
            ),
        ),
        rx.table.body(
            rx.foreach(State.users, show_user),
        ),
        variant="surface",
        size="3",
    )

Next let's add a form to the app so we can add new users to the table.

Using a Form to Add Data
We build a form using rx.form, which takes several components such as rx.input and rx.select, which represent the form fields that allow you to add information to submit with the form. Check out the form docs for more information on form components.

The rx.input component takes in several props. The placeholder prop is the text that is displayed in the input field when it is empty. The name prop is the name of the input field, which gets passed through in the dictionary when the form is submitted. The required prop is a boolean that determines if the input field is required.

The rx.select component takes in a list of options that are displayed in the dropdown. The other props used here are identical to the rx.input component.




Male

rx.form(
    rx.input(
        placeholder="User Name", name="name", required=True
    ),
    rx.input(
        placeholder="user@reflex.dev",
        name="email",
    ),
    rx.select(
        ["Male", "Female"],
        placeholder="Male",
        name="gender",
    ),
)

This form is all very compact as you can see from the example, so we need to add some styling to make it look better. We can do this by adding a vstack component around the form fields. The vstack component stacks the form fields vertically. Check out the layout docs for more information on how to layout your app.




Male

rx.form(
    rx.vstack(
        rx.input(
            placeholder="User Name",
            name="name",
            required=True,
        ),
        rx.input(
            placeholder="user@reflex.dev",
            name="email",
        ),
        rx.select(
            ["Male", "Female"],
            placeholder="Male",
            name="gender",
        ),
    ),
)

Now you have probably realised that we have all the form fields, but we have no way to submit the form. We can add a submit button to the form by adding a rx.button component to the vstack component. The rx.button component takes in the text that is displayed on the button and the type prop which is the type of button. The type prop is set to submit so that the form is submitted when the button is clicked.

In addition to this we need a way to update the users state variable when the form is submitted. All state changes are handled through functions in the state class, called event handlers.

Components have special props called event triggers, such as on_submit, that can be used to make components interactive. Event triggers connect components to event handlers, which update the state. Different event triggers expect the event handler that you hook them up to, to take in different arguments (and some do not take in any arguments).

The on_submit event trigger of rx.form is hooked up to the add_user event handler that is defined in the State class. This event trigger expects to pass a dict, containing the form data, to the event handler that it is hooked up to. The add_user event handler takes in the form data as a dictionary and appends it to the users state variable.

class State(rx.State):
    ...

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))


def form():
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="User Name",
                name="name",
                required=True,
            ),
            rx.input(
                placeholder="user@reflex.dev",
                name="email",
            ),
            rx.select(
                ["Male", "Female"],
                placeholder="Male",
                name="gender",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=State.add_user,
        reset_on_submit=True,
    )

Finally we must add the new form() component we have defined to the index() function so that the form is rendered on the page.

Below is the full code for the app so far. If you try this form out you will see that you can add new users to the table by filling out the form and clicking the submit button. The form data will also appear as a toast (a small window in the corner of the page) on the screen when submitted.




Male
Submit
Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
class State(rx.State):
    users: list[User] = [
        User(
            name="Danilo Sousa",
            email="danilo@example.com",
            gender="Male",
        ),
        User(
            name="Zahra Ambessa",
            email="zahra@example.com",
            gender="Female",
        ),
    ]

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))


def show_user(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
    )


def form():
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="User Name",
                name="name",
                required=True,
            ),
            rx.input(
                placeholder="user@reflex.dev",
                name="email",
            ),
            rx.select(
                ["Male", "Female"],
                placeholder="Male",
                name="gender",
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=State.add_user,
        reset_on_submit=True,
    )


def index() -> rx.Component:
    return rx.vstack(
        form(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                ),
            ),
            rx.table.body(
                rx.foreach(State.users, show_user),
            ),
            variant="surface",
            size="3",
        ),
    )

Putting the Form in an Overlay
In Reflex, we like to make the user interaction as intuitive as possible. Placing the form we just constructed in an overlay creates a focused interaction by dimming the background, and ensures a cleaner layout when you have multiple action points such as editing and deleting as well.

We will place the form inside of a rx.dialog component (also called a modal). The rx.dialog.root contains all the parts of a dialog, and the rx.dialog.trigger wraps the control that will open the dialog. In our case the trigger will be an rx.button that says "Add User" as shown below.

rx.dialog.trigger(
    rx.button(
        rx.icon("plus", size=26),
        rx.text("Add User", size="4"),
    ),
)

After the trigger we have the rx.dialog.content which contains everything within our dialog, including a title, a description and our form. The first way to close the dialog is without submitting the form and the second way is to close the dialog by submitting the form as shown below. This requires two rx.dialog.close components within the dialog.

rx.dialog.close(
    rx.button(
        "Cancel",
        variant="soft",
        color_scheme="gray",
    ),
),
rx.dialog.close(
    rx.button("Submit", type="submit"),
)

The total code for the dialog with the form in it is below.


Add User

rx.dialog.root(
    rx.dialog.trigger(
        rx.button(
            rx.icon("plus", size=26),
            rx.text("Add User", size="4"),
        ),
    ),
    rx.dialog.content(
        rx.dialog.title(
            "Add New User",
        ),
        rx.dialog.description(
            "Fill the form with the user's info",
        ),
        rx.form(
            # flex is similar to vstack and used to layout the form fields
            rx.flex(
                rx.input(
                    placeholder="User Name",
                    name="name",
                    required=True,
                ),
                rx.input(
                    placeholder="user@reflex.dev",
                    name="email",
                ),
                rx.select(
                    ["Male", "Female"],
                    placeholder="Male",
                    name="gender",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Submit", type="submit"),
                    ),
                    spacing="3",
                    justify="end",
                ),
                direction="column",
                spacing="4",
            ),
            on_submit=State3.add_user,
            reset_on_submit=False,
        ),
        # max_width is used to limit the width of the dialog
        max_width="450px",
    ),
)

At this point we have an app that allows you to add users to a table by filling out a form. The form is placed in a dialog that can be opened by clicking the "Add User" button. We change the name of the component from form to add_customer_button and update this in our index component. The full app so far and code are below.


Add User

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
class User(rx.Base):
    """The user model."""

    name: str
    email: str
    gender: str


class State(rx.State):
    users: list[User] = [
        User(
            name="Danilo Sousa",
            email="danilo@example.com",
            gender="Male",
        ),
        User(
            name="Zahra Ambessa",
            email="zahra@example.com",
            gender="Female",
        ),
    ]

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))


def show_user(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
    )


def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add New User",
            ),
            rx.dialog.description(
                "Fill the form with the user's info",
            ),
            rx.form(
                rx.flex(
                    rx.input(
                        placeholder="User Name",
                        name="name",
                        required=True,
                    ),
                    rx.input(
                        placeholder="user@reflex.dev",
                        name="email",
                    ),
                    rx.select(
                        ["Male", "Female"],
                        placeholder="Male",
                        name="gender",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Submit", type="submit"
                            ),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


def index() -> rx.Component:
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                ),
            ),
            rx.table.body(
                rx.foreach(State.users, show_user),
            ),
            variant="surface",
            size="3",
        ),
    )

Plotting Data in a Graph
The last part of this tutorial is to plot the user data in a graph. We will use Reflex's built-in graphing library recharts to plot the number of users of each gender.

Transforming the data for the graph
The graphing components in Reflex expect to take in a list of dictionaries. Each dictionary represents a data point on the graph and contains the x and y values. We will create a new event handler in the state called transform_data to transform the user data into the format that the graphing components expect. We must also create a new state variable called users_for_graph to store the transformed data, which will be used to render the graph.

from collections import Counter


class State(rx.State):
    users: list[User] = []
    users_for_graph: list[dict] = []

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))
        self.transform_data()

    def transform_data(self):
        """Transform user gender group data into a format suitable for visualization in graphs."""
        # Count users of each gender group
        gender_counts = Counter(
            user.gender for user in self.users
        )

        # Transform into list of dict so it can be used in the graph
        self.users_for_graph = [
            {"name": gender_group, "value": count}
            for gender_group, count in gender_counts.items()
        ]

As we can see above the transform_data event handler uses the Counter class from the collections module to count the number of users of each gender. We then create a list of dictionaries from this which we set to the state var users_for_graph.

Finally we can see that whenever we add a new user through submitting the form and running the add_user event handler, we call the transform_data event handler to update the users_for_graph state variable.

Rendering the graph
We use the rx.recharts.bar_chart component to render the graph. We pass through the state variable for our graphing data as data=State.users_for_graph. We also pass in a rx.recharts.bar component which represents the bars on the graph. The rx.recharts.bar component takes in the data_key prop which is the key in the data dictionary that represents the y value of the bar. The stroke and fill props are used to set the color of the bars.

The rx.recharts.bar_chart component also takes in rx.recharts.x_axis and rx.recharts.y_axis components which represent the x and y axes of the graph. The data_key prop of the rx.recharts.x_axis component is set to the key in the data dictionary that represents the x value of the bar. Finally we add width and height props to set the size of the graph.

def graph():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=State.users_for_graph,
        width="100%",
        height=250,
    )

Finally we add this graph() component to our index() component so that the graph is rendered on the page. The code for the full app with the graph included is below. If you try this out you will see that the graph updates whenever you add a new user to the table.


Add User

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
from collections import Counter


class State(rx.State):
    users: list[User] = [
        User(
            name="Danilo Sousa",
            email="danilo@example.com",
            gender="Male",
        ),
        User(
            name="Zahra Ambessa",
            email="zahra@example.com",
            gender="Female",
        ),
    ]
    users_for_graph: list[dict] = []

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))
        self.transform_data()

    def transform_data(self):
        """Transform user gender group data into a format suitable for visualization in graphs."""
        # Count users of each gender group
        gender_counts = Counter(
            user.gender for user in self.users
        )

        # Transform into list of dict so it can be used in the graph
        self.users_for_graph = [
            {"name": gender_group, "value": count}
            for gender_group, count in gender_counts.items()
        ]


def show_user(user: User):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
    )


def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add New User",
            ),
            rx.dialog.description(
                "Fill the form with the user's info",
            ),
            rx.form(
                rx.flex(
                    rx.input(
                        placeholder="User Name",
                        name="name",
                        required=True,
                    ),
                    rx.input(
                        placeholder="user@reflex.dev",
                        name="email",
                    ),
                    rx.select(
                        ["Male", "Female"],
                        placeholder="male",
                        name="gender",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Submit", type="submit"
                            ),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )


def graph():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=State.users_for_graph,
        width="100%",
        height=250,
    )


def index() -> rx.Component:
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                ),
            ),
            rx.table.body(
                rx.foreach(State.users, show_user),
            ),
            variant="surface",
            size="3",
        ),
        graph(),
    )

One thing you may have noticed about your app is that the graph does not appear initially when you run the app, and that you must add a user to the table for it to first appear. This occurs because the transform_data event handler is only called when a user is added to the table. In the next section we will explore a solution to this.

Final Cleanup
Revisiting app.add_page
At the beginning of this tutorial we mentioned that the app.add_page function is required for every Reflex app. This function is used to add a component to a page.

The app.add_page currently looks like this app.add_page(index). We could change the route that the page renders on by setting the route prop such as route="/custom-route", this would change the route to http://localhost:3000/custom-route for this page.

We can also set a title to be shown in the browser tab and a description as shown in search results.

To solve the problem we had above about our graph not loading when the page loads, we can use on_load inside of app.add_page to call the transform_data event handler when the page loads. This would look like on_load=State.transform_data. Below see what our app.add_page would look like with some of the changes above added.


Add User

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
app.add_page(
    index,
    title="Customer Data App",
    description="A simple app to manage customer data.",
    on_load=State.transform_data,
)

Revisiting app=rx.App()
At the beginning of the tutorial we also mentioned that we defined our app using app=rx.App(). We can also pass in some props to the rx.App component to customize the app.

The most important one is theme which allows you to customize the look and feel of the app. The theme prop takes in an rx.theme component which has several props that can be set.

The radius prop sets the global radius value for the app that is inherited by all components that have a radius prop. It can be overwritten locally for a specific component by manually setting the radius prop.

The accent_color prop sets the accent color of the app. Check out other options for the accent color here.

To see other props that can be set at the app level check out this documentation

app = rx.App(
    theme=rx.theme(radius="full", accent_color="grass"),
)

Unfortunately in this tutorial here we cannot actually apply this to the live example on the page, but if you copy and paste the code below into a reflex app locally you can see it in action.

Conclusion
Finally let's make some final styling updates to our app. We will add some hover styling to the table rows and center the table inside the show_user with style=\{"_hover": {"bg": rx.color("gray", 3)}}, align="center".

In addition, we will add some width="100%" and align="center" to the index() component to center the items on the page and ensure they stretch the full width of the page.

Check out the full code and interactive app below:


Add User

Name	Email	Gender
Danilo Sousa	danilo@example.com	Male
Zahra Ambessa	zahra@example.com	Female
Male
Female
0
0.25
0.5
0.75
1
import reflex as rx
from collections import Counter

class User(rx.Base):
    """The user model."""

    name: str
    email: str
    gender: str


class State(rx.State):
    users: list[User] = [
        User(name="Danilo Sousa", email="danilo@example.com", gender="Male"),
        User(name="Zahra Ambessa", email="zahra@example.com", gender="Female"),
    ]
    users_for_graph: list[dict] = []

    def add_user(self, form_data: dict):
        self.users.append(User(**form_data))
        self.transform_data()
    
    def transform_data(self):
        """Transform user gender group data into a format suitable for visualization in graphs."""
        # Count users of each gender group
        gender_counts = Counter(user.gender for user in self.users)
        
        # Transform into list of dict so it can be used in the graph
        self.users_for_graph = [
            {
                "name": gender_group,
                "value": count
            }
            for gender_group, count in gender_counts.items()
        ]
        

def show_user(user: User):
    """Show a user in a table row."""
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        style=\{"_hover": 
            {"bg": rx.color("gray", 3)}
        },
        align="center",
    )

def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                "Add New User",
            ),
            rx.dialog.description(
                "Fill the form with the user's info",
            ),
            rx.form(
                rx.flex(
                    rx.input(
                        placeholder="User Name", name="name", required=True
                    ),
                    rx.input(
                        placeholder="user@reflex.dev",
                        name="email",
                    ),
                    rx.select(
                        ["Male", "Female"],
                        placeholder="male",
                        name="gender",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Submit", type="submit"
                            ),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=State.add_user,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
    )

def graph():
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=State.users_for_graph,
        width="100%",
        height=250,
    )

def index() -> rx.Component:
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Gender"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    State.users, show_user
                ),
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        graph(),
        align="center",
        width="100%",
    )


app = rx.App(
    theme=rx.theme(
        radius="full", accent_color="grass"
    ),
)

app.add_page(
    index,
    title="Customer Data App",
    description="A simple app to manage customer data.",
    on_load=State.transform_data,
)

And that is it for your first dashboard tutorial. In this tutorial we have created

a table to display user data
a form to add new users to the table
a dialog to showcase the form
a graph to visualize the user data
In addition to the above we have we have

explored state to allow you to show dynamic data that changes over time
explored events to allow you to make your app interactive and respond to user actions
added styling to the app to make it look better
Advanced Section (Hooking this up to a Database)
Coming Soon!

Interactive Tutorial: AI Chat App
This tutorial will walk you through building an AI chat app with Reflex. This app is fairly complex, but don't worry - we'll break it down into small steps.

You can find the full source code for this app here.

What You'll Learn
In this tutorial you'll learn how to:

Install reflex and set up your development environment.
Create components to define and style your UI.
Use state to add interactivity to your app.
Deploy your app to share with others.
Setting up Your Project

Video: Example of Setting up the Chat App

We will start by creating a new project and setting up our development environment. First, create a new directory for your project and navigate to it.

~ $ mkdir chatapp
~ $ cd chatapp

Next, we will create a virtual environment for our project. This is optional, but recommended. In this example, we will use venv to create our virtual environment.

chatapp $ python3 -m venv venv
$ source venv/bin/activate

Now, we will install Reflex and create a new project. This will create a new directory structure in our project directory.

Note: When prompted to select a template, choose option 0 for a blank project.

chatapp $ pip install reflex
chatapp $ reflex init
────────────────────────────────── Initializing chatapp ───────────────────────────────────
Success: Initialized chatapp
chatapp $ ls
assets          chatapp         rxconfig.py     venv

You can run the template app to make sure everything is working.

chatapp $ reflex run
─────────────────────────────────── Starting Reflex App ───────────────────────────────────
Compiling:  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 1/1 0:00:00
─────────────────────────────────────── App Running ───────────────────────────────────────
App running at: http://localhost:3000

You should see your app running at http://localhost:3000.

Reflex also starts the backend server which handles all the state management and communication with the frontend. You can test the backend server is running by navigating to http://localhost:8000/ping.

Now that we have our project set up, in the next section we will start building our app!

Basic Frontend
Let's start with defining the frontend for our chat app. In Reflex, the frontend can be broken down into independent, reusable components. See the components docs for more information.

Display A Question And Answer
We will modify the index function in chatapp/chatapp.py file to return a component that displays a single question and answer.

What is Reflex?
A way to build web apps in pure Python!
# chatapp.py

import reflex as rx


def index() -> rx.Component:
    return rx.container(
        rx.box(
            "What is Reflex?",
            # The user's question is on the right.
            text_align="right",
        ),
        rx.box(
            "A way to build web apps in pure Python!",
            # The answer is on the left.
            text_align="left",
        ),
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)

Components can be nested inside each other to create complex layouts. Here we create a parent container that contains two boxes for the question and answer.

We also add some basic styling to the components. Components take in keyword arguments, called props, that modify the appearance and functionality of the component. We use the text_align prop to align the text to the left and right.

Reusing Components
Now that we have a component that displays a single question and answer, we can reuse it to display multiple questions and answers. We will move the component to a separate function question_answer and call it from the index function.

What is Reflex?
A way to build web apps in pure Python!
What can I make with it?
Anything from a simple website to a complex web app!
def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(question, text_align="right"),
        rx.box(answer, text_align="left"),
        margin_y="1em",
    )


def chat() -> rx.Component:
    qa_pairs = [
        (
            "What is Reflex?",
            "A way to build web apps in pure Python!",
        ),
        (
            "What can I make with it?",
            "Anything from a simple website to a complex web app!",
        ),
    ]
    return rx.box(
        *[
            qa(question, answer)
            for question, answer in qa_pairs
        ]
    )


def index() -> rx.Component:
    return rx.container(chat())

Chat Input
Now we want a way for the user to input a question. For this, we will use the input component to have the user add text and a button component to submit the question.

What is Reflex?
A way to build web apps in pure Python!
What can I make with it?
Anything from a simple website to a complex web app!

Ask
def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ask a question"),
        rx.button("Ask"),
    )


def index() -> rx.Component:
    return rx.container(
        chat(),
        action_bar(),
    )

Styling
Let's add some styling to the app. More information on styling can be found in the styling docs. To keep our code clean, we will move the styling to a separate file chatapp/style.py.

# style.py
import reflex as rx

# Common styles for questions and answers.
shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)

# Set specific styles for questions and answers.
question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4),
)
answer_style = message_style | dict(
    margin_right=chat_margin,
    background_color=rx.color("accent", 8),
)

# Styles for the action bar.
input_style = dict(
    border_width="1px",
    padding="0.5em",
    box_shadow=shadow,
    width="350px",
)
button_style = dict(
    background_color=rx.color("accent", 10),
    box_shadow=shadow,
)

We will import the styles in chatapp.py and use them in the components. At this point, the app should look like this:

What is Reflex?
A way to build web apps in pure Python!
What can I make with it?
Anything from a simple website to a complex web app!

Ask
# chatapp.py
import reflex as rx

from chatapp import style


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align="left",
        ),
        margin_y="1em",
        width="100%",
    )


def chat() -> rx.Component:
    qa_pairs = [
        (
            "What is Reflex?",
            "A way to build web apps in pure Python!",
        ),
        (
            "What can I make with it?",
            "Anything from a simple website to a complex web app!",
        ),
    ]
    return rx.box(
        *[
            qa(question, answer)
            for question, answer in qa_pairs
        ]
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Ask a question",
            style=style.input_style,
        ),
        rx.button("Ask", style=style.button_style),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            align="center",
        )
    )


app = rx.App()
app.add_page(index)

The app is looking good, but it's not very useful yet! In the next section, we will add some functionality to the app.

State
Now let’s make the chat app interactive by adding state. The state is where we define all the variables that can change in the app and all the functions that can modify them. You can learn more about state in the state docs.

Defining State
We will create a new file called state.py in the chatapp directory. Our state will keep track of the current question being asked and the chat history. We will also define an event handler answer which will process the current question and add the answer to the chat history.

# state.py
import reflex as rx


class State(rx.State):
    # The current question being asked.
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    @rx.event
    def answer(self):
        # Our chatbot is not very smart right now...
        answer = "I don't know!"
        self.chat_history.append((self.question, answer))

Binding State to Components
Now we can import the state in chatapp.py and reference it in our frontend components. We will modify the chat component to use the state instead of the current fixed questions and answers.


Ask
# chatapp.py
from chatapp.state import State

...


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


...


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )

Normal Python for loops don't work for iterating over state vars because these values can change and aren't known at compile time. Instead, we use the foreach component to iterate over the chat history.

We also bind the input's on_change event to the set_question event handler, which will update the question state var while the user types in the input. We bind the button's on_click event to the answer event handler, which will process the question and add the answer to the chat history. The set_question event handler is a built-in implicitly defined event handler. Every base var has one. Learn more in the events docs under the Setters section.

Clearing the Input
Currently the input doesn't clear after the user clicks the button. We can fix this by binding the value of the input to question, with value=State.question, and clear it when we run the event handler for answer, with self.question = ''.


Ask
# chatapp.py
def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )

# state.py


@rx.event
def answer(self):
    # Our chatbot is not very smart right now...
    answer = "I don't know!"
    self.chat_history.append((self.question, answer))
    self.question = ""

Streaming Text
Normally state updates are sent to the frontend when an event handler returns. However, we want to stream the text from the chatbot as it is generated. We can do this by yielding from the event handler. See the yield events docs for more info.


Ask
# state.py
import asyncio

...


async def answer(self):
    # Our chatbot is not very smart right now...
    answer = "I don't know!"
    self.chat_history.append((self.question, ""))

    # Clear the question input.
    self.question = ""
    # Yield here to clear the frontend input before continuing.
    yield

    for i in range(len(answer)):
        # Pause to show the streaming effect.
        await asyncio.sleep(0.1)
        # Add one letter at a time to the output.
        self.chat_history[-1] = (
            self.chat_history[-1][0],
            answer[: i + 1],
        )
        yield

In the next section, we will finish our chatbot by adding AI!

Final App
We will use OpenAI's API to give our chatbot some intelligence.

Configure the OpenAI API Key
Ensure you have an active OpenAI subscription. Save your API key as an environment variable named OPENAI_API_KEY:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Install the openai pypi package:

```bash
pip install openai
```

Using the API
We need to modify our event handler to send a request to the API.


Ask
# state.py
import os

from openai import AsyncOpenAI


@rx.event
async def answer(self):
    # Our chatbot has some brains now!
    client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    session = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": self.question}
        ],
        stop=None,
        temperature=0.7,
        stream=True,
    )

    # Add to the answer as the chatbot responds.
    answer = ""
    self.chat_history.append((self.question, answer))

    # Clear the question input.
    self.question = ""
    # Yield here to clear the frontend input before continuing.
    yield

    async for item in session:
        if hasattr(item.choices[0].delta, "content"):
            if item.choices[0].delta.content is None:
                # presence of 'None' indicates the end of the response
                break
            answer += item.choices[0].delta.content
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer,
            )
            yield

Finally, we have our chatbot!

Final Code
We wrote all our code in three files, which you can find below.

# chatapp.py
import reflex as rx

from chatapp import style
from chatapp.state import State


def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align="left",
        ),
        margin_y="1em",
    )


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        )
    )


def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            align="center",
        )
    )


app = rx.App()
app.add_page(index)

# state.py
import os

from openai import AsyncOpenAI

import reflex as rx


class State(rx.State):
    # The current question being asked.
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    async def answer(self):
        # Our chatbot has some brains now!
        client = AsyncOpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )

        session = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": self.question}
            ],
            stop=None,
            temperature=0.7,
            stream=True,
        )

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))

        # Clear the question input.
        self.question = ""
        # Yield here to clear the frontend input before continuing.
        yield

        async for item in session:
            if hasattr(item.choices[0].delta, "content"):
                if item.choices[0].delta.content is None:
                    # presence of 'None' indicates the end of the response
                    break
                answer += item.choices[0].delta.content
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                )
                yield

# style.py
import reflex as rx

# Common styles for questions and answers.
shadow = "rgba(0, 0, 0, 0.15) 0px 2px 8px"
chat_margin = "20%"
message_style = dict(
    padding="1em",
    border_radius="5px",
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="30em",
    display="inline-block",
)

# Set specific styles for questions and answers.
question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4),
)
answer_style = message_style | dict(
    margin_right=chat_margin,
    background_color=rx.color("accent", 8),
)

# Styles for the action bar.
input_style = dict(
    border_width="1px",
    padding="0.5em",
    box_shadow=shadow,
    width="350px",
)
button_style = dict(
    background_color=rx.color("accent", 10),
    box_shadow=shadow,
)

Next Steps
Congratulations! You have built your first chatbot. From here, you can read through the rest of the documentations to learn about Reflex in more detail. The best way to learn is to build something, so try to build your own app using this as a starting point!

One More Thing
With our hosting service, you can deploy this app with a single command within minutes. Check out our Hosting Quick Start.

How Reflex Works
We'll use the following basic app that displays Github profile images as an example to explain the different parts of the architecture.



import requests
import reflex as rx


class GithubState(rx.State):
    url: str = "https://github.com/reflex-dev"
    profile_image: str = (
        "https://avatars.githubusercontent.com/u/104714959"
    )

    @rx.event
    def set_profile(self, username: str):
        if username == "":
            return
        github_data = requests.get(
            f"https://api.github.com/users/{username}"
        ).json()
        self.url = github_data["url"]
        self.profile_image = github_data["avatar_url"]


def index():
    return rx.hstack(
        rx.link(
            rx.avatar(src=GithubState.profile_image),
            href=GithubState.url,
        ),
        rx.input(
            placeholder="Your Github username",
            on_blur=GithubState.set_profile,
        ),
    )

The Reflex Architecture
Full-stack web apps are made up of a frontend and a backend. The frontend is the user interface, and is served as a web page that runs on the user's browser. The backend handles the logic and state management (such as databases and APIs), and is run on a server.

In traditional web development, these are usually two separate apps, and are often written in different frameworks or languages. For example, you may combine a Flask backend with a React frontend. With this approach, you have to maintain two separate apps and end up writing a lot of boilerplate code to connect the frontend and backend.

We wanted to simplify this process in Reflex by defining both the frontend and backend in a single codebase, while using Python for everything. Developers should only worry about their app's logic and not about the low-level implementation details.

TLDR
Under the hood, Reflex apps compile down to a React frontend app and a FastAPI backend app. Only the UI is compiled to Javascript; all the app logic and state management stays in Python and is run on the server. Reflex uses WebSockets to send events from the frontend to the backend, and to send state updates from the backend to the frontend.

The diagram below provides a detailed overview of how a Reflex app works. We'll go through each part in more detail in the following sections.



Frontend
We wanted Reflex apps to look and feel like a traditional web app to the end user, while still being easy to build and maintain for the developer. To do this, we built on top of mature and popular web technologies.

When you reflex run your app, Reflex compiles the frontend down to a single-page Next.js app and serves it on a port (by default 3000) that you can access in your browser.

The frontend's job is to reflect the app's state, and send events to the backend when the user interacts with the UI. No actual logic is run on the frontend.

Components
Reflex frontends are built using components that can be composed together to create complex UIs. Instead of using a templating language that mixes HTML and Python, we just use Python functions to define the UI.

def index():
    return rx.hstack(
        rx.link(
            rx.avatar(src=GithubState.profile_image),
            href=GithubState.url,
        ),
        rx.input(
            placeholder="Your Github username",
            on_blur=GithubState.set_profile,
        ),
    )

In our example app, we have components such as rx.hstack, rx.avatar, and rx.input. These components can have different props that affect their appearance and functionality - for example the rx.input component has a placeholder prop to display the default text.

We can make our components respond to user interactions with events such as on_blur, which we will discuss more below.

Under the hood, these components compile down to React components. For example, the above code compiles down to the following React code:

<HStack>
    <Link href={GithubState.url}>
        <Avatar src={GithubState.profile_image}/>
    </Link>
    <Input
        placeholder="Your Github username"
        // This would actually be a websocket call to the backend.
        onBlur={GithubState.set_profile}
    >
</HStack>

Many of our core components are based on Radix, a popular React component library. We also have many other components for graphing, datatables, and more.

We chose React because it is a popular library with a huge ecosystem. Our goal isn't to recreate the web ecosystem, but to make it accessible to Python developers.

This also lets our users bring their own components if we don't have a component they need. Users can wrap their own React components and then publish them for others to use. Over time we will build out our third party component ecosystem so that users can easily find and use components that others have built.

Styling
We wanted to make sure Reflex apps look good out of the box, while still giving developers full control over the appearance of their app.

We have a core theming system that lets you set high level styling options such as dark mode and accent color throughout your app to give it a unified look and feel.

Beyond this, Reflex components can be styled using the full power of CSS. We leverage the Emotion library to allow "CSS-in-Python" styling, so you can pass any CSS prop as a keyword argument to a component. This includes responsive props by passing a list of values.

Backend
Now let's look at how we added interactivity to our apps.

In Reflex only the frontend compiles to Javascript and runs on the user's browser, while all the state and logic stays in Python and is run on the server. When you reflex run, we start a FastAPI server (by default on port 8000) that the frontend connects to through a websocket.

All the state and logic are defined within a State class.

class GithubState(rx.State):
    url: str = "https://github.com/reflex-dev"
    profile_image: str = (
        "https://avatars.githubusercontent.com/u/104714959"
    )

    def set_profile(self, username: str):
        if username == "":
            return
        github_data = requests.get(
            f"https://api.github.com/users/{username}"
        ).json()
        self.url = github_data["url"]
        self.profile_image = github_data["avatar_url"]

The state is made up of vars and event handlers.

Vars are any values in your app that can change over time. They are defined as class attributes on your State class, and may be any Python type that can be serialized to JSON. In our example, url and profile_image are vars.

Event handlers are methods in your State class that are called when the user interacts with the UI. They are the only way that we can modify the vars in Reflex, and can be called in response to user actions, such as clicking a button or typing in a text box. In our example, set_profile is an event handler that updates the url and profile_image vars.

Since event handlers are run on the backend, you can use any Python library within them. In our example, we use the requests library to make an API call to Github to get the user's profile image.

Event Processing
Now we get into the interesting part - how we handle events and state updates.

Normally when writing web apps, you have to write a lot of boilerplate code to connect the frontend and backend. With Reflex, you don't have to worry about that - we handle the communication between the frontend and backend for you. Developers just have to write their event handler logic, and when the vars are updated the UI is automatically updated.

You can refer to the diagram above for a visual representation of the process. Let's walk through it with our Github profile image example.

Event Triggers
The user can interact with the UI in many ways, such as clicking a button, typing in a text box, or hovering over an element. In Reflex, we call these event triggers.

rx.input(
    placeholder="Your Github username",
    on_blur=GithubState.set_profile,
)

In our example we bind the on_blur event trigger to the set_profile event handler. This means that when the user types in the input field and then clicks away, the set_profile event handler is called.

Event Queue
On the frontend, we maintain an event queue of all pending events. An event consists of three major pieces of data:

client token: Each client (browser tab) has a unique token to identify it. This let's the backend know which state to update.
event handler: The event handler to run on the state.
arguments: The arguments to pass to the event handler.
Let's assume I type my username "picklelo" into the input. In this example, our event would look something like this:

{
  "client_token": "abc123",
  "event_handler": "GithubState.set_profile",
  "arguments": ["picklelo"]
}

On the frontend, we maintain an event queue of all pending events.

When an event is triggered, it is added to the queue. We have a processing flag to make sure only one event is processed at a time. This ensures that the state is always consistent and there aren't any race conditions with two event handlers modifying the state at the same time.

There are exceptions to this, such as background events which allow you to run events in the background without blocking the UI.

Once the event is ready to be processed, it is sent to the backend through a WebSocket connection.

State Manager
Once the event is received, it is processed on the backend.

Reflex uses a state manager which maintains a mapping between client tokens and their state. By default, the state manager is just an in-memory dictionary, but it can be extended to use a database or cache. In production we use Redis as our state manager.

Event Handling
Once we have the user's state, the next step is to run the event handler with the arguments.

def set_profile(self, username: str):
    if username == "":
        return
    github_data = requests.get(
        f"https://api.github.com/users/{username}"
    ).json()
    self.url = github_data["url"]
    self.profile_image = github_data["avatar_url"]

In our example, the set_profile event handler is run on the user's state. This makes an API call to Github to get the user's profile image, and then updates the state's url and profile_image vars.

State Updates
Every time an event handler returns (or yields), we save the state in the state manager and send the state updates to the frontend to update the UI.

To maintain performance as your state grows, internally Reflex keeps track of vars that were updated during the event handler (dirty vars). When the event handler is done processing, we find all the dirty vars and create a state update to send to the frontend.

In our case, the state update may look something like this:

{
  "url": "https://github.com/picklelo",
  "profile_image": "https://avatars.githubusercontent.com/u/104714959"
}

We store the new state in our state manager, and then send the state update to the frontend. The frontend then updates the UI to reflect the new state. In our example, the new Github profile image is displayed.

Configuration
Reflex apps can be configured using a configuration file, environment variables, and command line arguments.

Configuration File
Running reflex init will create an rxconfig.py file in your root directory. You can pass keyword arguments to the Config class to configure your app.

For example:

# rxconfig.py
import reflex as rx

config = rx.Config(
    app_name="my_app_name",
    # Connect to your own database.
    db_url="postgresql://user:password@localhost:5432/my_db",
    # Change the frontend port.
    frontend_port=3001,
)

See the config reference for all the parameters available.

Environment Variables
You can override the configuration file by setting environment variables. For example, to override the frontend_port setting, you can set the FRONTEND_PORT environment variable.

FRONTEND_PORT=3001 reflex run

Command Line Arguments
Finally, you can override the configuration file and environment variables by passing command line arguments to reflex run.

reflex run --frontend-port 3001

See the CLI reference for all the arguments available.

Customizable App Data Directory
The REFLEX_DIR environment variable can be set, which allows users to set the location where Reflex writes helper tools like Bun and NodeJS.

By default we use Platform specific directories:

On windows, C:/Users/<username>/AppData/Local/reflex is used.

On macOS, ~/Library/Application Support/reflex is used.

On linux, ~/.local/share/reflex is used.

Project Structure (Advanced)
App Module
Reflex imports the main app module based on the app_name from the config, which must define a module-level global named app as an instance of rx.App.

The main app module is responsible for importing all other modules that make up the app and defining app = rx.App().

All other modules containing pages, state, and models MUST be imported by the main app module or package for Reflex to include them in the compiled output.

Breaking the App into Smaller Pieces
As applications scale, effective organization is crucial. This is achieved by breaking the application down into smaller, manageable modules and organizing them into logical packages that avoid circular dependencies.

In the following documentation there will be an app with an app_name of example_big_app. The main module would be example_big_app/example_big_app.py.

In the Putting it all together section there is a visual of the project folder structure to help follow along with the examples below.

Pages Package:
All complex apps will have multiple pages, so it is recommended to create example_big_app/pages as a package.

This package should contain one module per page in the app.
If a particular page depends on the state, the substate should be defined in the same module as the page.
The page-returning function should be decorated with rx.page() to have it added as a route in the app.
import reflex as rx

from ..state import AuthState


class LoginState(AuthState):
    @rx.event
    def handle_submit(self, form_data):
        self.logged_in = authenticate(
            form_data["username"], form_data["password"]
        )


def login_field(name: str, **input_props):
    return rx.hstack(
        rx.text(name.capitalize()),
        rx.input(name=name, **input_props),
        width="100%",
        justify="between",
    )


@rx.page(route="/login")
def login():
    return rx.card(
        rx.form(
            rx.vstack(
                login_field("username"),
                login_field("password", type="password"),
                rx.button("Login"),
                width="100%",
                justify="center",
            ),
            on_submit=LoginState.handle_submit,
        ),
    )

Templating:
Most applications maintain a consistent layout and structure across pages. Defining this common structure in a separate module facilitates easy sharing and reuse when constructing individual pages.

Best Practices

Factor out common frontend UI elements into a function that returns a component.
If a function accepts a function that returns a component, it can be used as a decorator as seen below.
from typing import Callable

import reflex as rx

from .components.menu import menu
from .components.navbar import navbar


def template(
    page: Callable[[], rx.Component]
) -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.hstack(
            menu(),
            rx.container(page()),
        ),
        width="100%",
    )

The @template decorator should appear below the @rx.page decorator and above the page-returning function. See the Posts Page code for an example.

State Management
Most pages will use State in some capacity. You should avoid adding vars to a shared state that will only be used in a single page. Instead, define a new subclass of rx.State and keep it in the same module as the page.

Accessing other States
As of Reflex 0.4.3, any event handler can get access to an instance of any other substate via the get_state API. From a practical perspective, this means that state can be split up into smaller pieces without requiring a complex inheritance hierarchy to share access to other states.

In previous releases, if an app wanted to store settings in SettingsState with a page or component for modifying them, any other state with an event handler that needed to access those settings would have to inherit from SettingsState, even if the other state was mostly orthogonal. The other state would also now always have to load the settings, even for event handlers that didn't need to access them.

A better strategy is to load the desired state on demand from only the event handler which needs access to the substate.

A Settings Component:
import reflex as rx


class SettingsState(rx.State):
    refresh_interval: int = 15
    auto_update: bool = True
    prefer_plain_text: bool = True
    posts_per_page: int = 20


def settings_dialog():
    return rx.dialog(...)

A Post Page:
This page loads the SettingsState to determine how many posts to display per page and how often to refresh.

import reflex as rx

from ..models import Post
from ..template import template
from ..components.settings import SettingsState


class PostsState(rx.State):
    refresh_tick: int
    page: int
    posts: list[Post]

    @rx.event
    async def on_load(self):
        settings = await self.get_state(SettingsState)
        if settings.auto_update:
            self.refresh_tick = (
                settings.refresh_interval * 1000
            )
        else:
            self.refresh_tick = 0

    @rx.event
    async def tick(self, _):
        settings = await self.get_state(SettingsState)
        with rx.session() as session:
            q = (
                Post.select()
                .offset(self.page * settings.posts_per_page)
                .limit(settings.posts_per_page)
            )
            self.posts = q.all()

    @rx.event
    def go_to_previous(self):
        if self.page > 0:
            self.page = self.page - 1

    @rx.event
    def go_to_next(self):
        if self.posts:
            self.page = self.page + 1


@rx.page(route="/posts", on_load=PostsState.on_load)
@template
def posts():
    return rx.vstack(
        rx.foreach(PostsState.posts, post_view),
        rx.hstack(
            rx.button(
                "< Prev", on_click=PostsState.go_to_previous
            ),
            rx.button(
                "Next >", on_click=PostsState.go_to_next
            ),
            justify="between",
        ),
        rx.moment(
            interval=PostsState.refresh_tick,
            on_change=PostsState.tick,
            display="none",
        ),
        width="100%",
    )

Common State:
Common states and substates that are shared by multiple pages or components should be implemented in a separate module to avoid circular imports. This module should not import other modules in the app.

Component Reusability
The primary mechanism for reusing components in Reflex is to define a function that returns the component, then simply call it where that functionality is needed.

Component functions typically should not take any State classes as arguments, but prefer to import the needed state and access the vars on the class directly.

Memoize Functions for Improved Performance
In a large app, if a component has many subcomponents or is used in a large number of places, it can improve compile and runtime performance to memoize the function with the @lru_cache decorator.

To memoize the foo component to avoid re-creating it many times simply add @lru_cache to the function definition, and the component will only be created once per unique set of arguments.

from functools import lru_cache

import reflex as rx


class State(rx.State):
    v: str = "foo"


@lru_cache
def foo():
    return rx.text(State.v)


def index():
    return rx.flex(
        rx.button(
            "Change",
            on_click=State.set_v(
                rx.cond(State.v != "bar", "bar", "foo")
            ),
        ),
        *[foo() for _ in range(100)],
        direction="row",
        wrap="wrap",
    )

example_big_app/components
This package contains reusable parts of the app, for example headers, footers, and menus. If a particular component requires state, the substate may be defined in the same module for locality. Any substate defined in a component module should only contain fields and event handlers pertaining to that individual component.

External Components
Reflex 0.4.3 introduced support for the reflex component CLI commands, which makes it easy to bundle up common functionality to publish on PyPI as a standalone Python package that can be installed and used in any Reflex app.

When wrapping npm components or other self-contained bits of functionality, it can be helpful to move this complexity outside the app itself for easier maintenance and reuse in other apps.

Database Models:
It is recommended to implement all database models in a single file to make it easier to define relationships and understand the entire schema.

However, if the schema is very large, it might make sense to have a models package with individual models defined in their own modules.

At any rate, defining the models separately allows any page or component to import and use them without circular imports.

Top-level Package:
This is a great place to import all state, models, and pages that should be part of the app. Typically, components and helpers do not need to imported, because they will be imported by pages that use them (or they would be unused).

from . import state, models
from .pages import (
    index,
    login,
    post,
    product,
    profile,
    schedule,
)

__all__ = [
    "state",
    "models",
    "index",
    "login",
    "post",
    "product",
    "profile",
    "schedule",
]

If any pages are not imported here, they will not be compiled as part of the app.

example_big_app/example_big_app.py
This is the main app module. Since everything else is defined in other modules, this file becomes very simple.

import reflex as rx

app = rx.App()

File Management
There are two categories of non-code assets (media, fonts, stylesheets, documents) typically used in a Reflex app.

assets
The assets directory is used for static files that should be accessible relative to the root of the frontend (default port 3000). When an app is deployed in production mode, changes to the assets directory will NOT be available at runtime!

When referencing an asset, always use a leading forward slash, so the asset can be resolved regardless of the page route where it may appear.

uploaded_files
If an app needs to make files available dynamically at runtime, it is recommended to set the target directory via REFLEX_UPLOADED_FILES_DIR environment variable (default ./uploaded_files), write files relative to the path returned by rx.get_upload_dir(), and create working links via rx.get_upload_url(relative_path).

Uploaded files are served from the backend (default port 8000) via /_upload/<relative_path>

Putting it all together
Based on the previous discussion, the recommended project layout look like this.

example-big-app/
├─ assets/
├─ example_big_app/
│  ├─ components/
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  ├─ footer.py
│  │  ├─ menu.py
│  │  ├─ navbar.py
│  ├─ pages/
│  │  ├─ __init__.py
│  │  ├─ index.py
│  │  ├─ login.py
│  │  ├─ posts.py
│  │  ├─ product.py
│  │  ├─ profile.py
│  │  ├─ schedule.py
│  ├─ __init__.py
│  ├─ example_big_app.py
│  ├─ models.py
│  ├─ state.py
│  ├─ template.py
├─ uploaded_files/
├─ requirements.txt
├─ rxconfig.py

Key Takeaways
Like any other Python project, split up the app into modules and packages to keep the codebase organized and manageable.
Using smaller modules and packages makes it easier to reuse components and state across the app without introducing circular dependencies.
Create individual functions to encapsulate units of functionality and reuse them where needed.
