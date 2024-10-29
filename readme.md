# CSCI-2910 Discord Task Manager Bot

This is a Discord bot that allows users to create, view, update, and delete tasks directly within a Discord server. It integrates with FastAPI for handling API requests and uses SQLite as its database to store tasks.

## Features

- **Create Task**: Add new tasks with a title, description, and optional due date.
- **View Tasks**: Retrieve a list of your tasks or view all tasks in the database.
- **Update Task**: Modify existing tasks by updating the title, description, due date, or status.
- **Delete Task**: Remove a task from the database.
- **API Integration**: Uses FastAPI for backend functionality.
- **Persistent Storage**: Stores task data in an SQLite database.

## Prerequisites

- Python 3.8+
- Discord account and server
- Discord bot token (stored in `.env` file)
- FastAPI and SQLite for the backend

## Getting Started

1. **Clone the repository** and navigate to the project folder.
2. **Install dependencies**:
   ```bash
   pip install discord.py aiohttp fastapi uvicorn python-dotenv
   ```
3. **Create a `.env` file in the main project folder and add your Discord bot token**:
   ```plaintext
   TOKEN=your_discord_bot_token
   ```
4. **Run the FastAPI server for handling API requests (Run this command from inside the "API" folder)**:
   ```bash
   uvicorn main:app --reload
   ```
5. **Start the Discord bot by running this command in the main folder**:
   ```bash
   python main.py
   ```

## Usage

Once the bot is running, you can use the following commands in Discord:

- `/createtask <title> <description> <due_date>`: Creates a new task with the specified title, description, and optional due date.

- `/viewtasks`: Displays a list of tasks specific to the user.

- `/viewalltasks`: Shows all tasks across users.

- `/updatetask <task_id> <title> <description> <due_date> <status>`: Updates an existing task with the given ID and specified details.

- `/deletetask <task_id>`: Deletes a task by its ID.
