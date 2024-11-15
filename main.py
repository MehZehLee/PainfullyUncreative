import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import aiohttp

intents = discord.Intents.default() 
intents.message_content = True 

bot = commands.Bot(command_prefix='/', intents=intents)
tree = bot.tree

class TaskCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /createtask <title> <description> <priority> <due_date>
    @app_commands.command(name='createtask', description='Create a new task')
    async def create_task(self, interaction: discord.Interaction, title: str, description: str = None, priority: str = None, due_date: str = None):
        async with aiohttp.ClientSession() as session:
            json_data = {'user_id': interaction.user.id,
                        'title': title,
                        'description': description,
                        'priority': priority}
            
            # Default due_date to None if not specified
            if due_date is not None:
                json_data['due_date'] = due_date

            # Default priority to Medium if not specified
            if priority is None:
                json_data['priority'] = "Medium"
            # Check if priority is valid (Low, Medium, High)
            elif priority != "Low" and priority != "Medium" and priority != "High":
                await interaction.response.send_message(f"Invalid priority. Please enter 'Low', 'Medium', or 'High'.")
                return

            async with session.post("http://localhost:8000/createtask", json=json_data) as response:
                if response.status == 200:
                    await interaction.response.send_message(f"Task created successfully!")
                    await interaction.followup.send(f"Title: {title}\nDescription: {description}\nPriority: {priority}\nDue Date: {due_date}")
                else:
                    await interaction.response.send_message(f"Error creating task.")
                    print(await response.text())

    # /viewtasks
    @app_commands.command(name='viewtasks', description='View your tasks')
    async def view_tasks(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:8000/gettasks/{interaction.user.id}") as response:
                if response.status == 200:
                    tasks = await response.json()
                    task_list = "\n".join([f"{task['task_id']}: {task['title']} - {task['description']} - {task['status']}" for task in tasks])
                    if task_list == "":
                        task_list = "No tasks found."
                    await interaction.response.send_message(f"**Your Tasks:**\n**ID | Title | Description | Status**\n{task_list}")
                else:
                    await interaction.response.send_message(f"Error retrieving tasks.")
                    print(await response.text())

    # /viewalltasks
    # Manage Server permission required
    @app_commands.command(name='viewalltasks', description='View all tasks')
    @commands.has_permissions(manage_guild=True)
    async def view_all_tasks(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/gettasks") as response:
                if response.status == 200:
                    tasks = await response.json()
                    task_list = "\n".join([f"{task['task_id']}: {task['title']} - {task['description']} - {task['status']}" for task in tasks])
                    if task_list == "":
                        task_list = "No tasks found."
                    await interaction.response.send_message(f"**All Tasks:**\n**ID | Title | Description | Status**\n{task_list}")
                else:
                    await interaction.response.send_message(f"Error retrieving tasks.")
                    print(await response.text())

    # /updatetask <task_id> <title> <description> <due_date> <status>
    @app_commands.command(name='updatetask', description='Update an existing task')
    async def update_task(self, interaction: discord.Interaction, task_id: int, title: str = None, description: str = None, due_date: str = None, status: str = None):
        async with aiohttp.ClientSession() as session:
            data = {'title': title, 'description': description, 'due_date': due_date, 'status': status}
            async with session.patch(f"http://localhost:8000/updatetask/{task_id}", json=data) as response:
                if response.status == 200:
                    await interaction.response.send_message(f"Task #{task_id} updated successfully!")
                else:
                    await interaction.response.send_message(f"Error updating task.")
                    print(await response.text())

    # /updatestatus <task_id> <status>
    # Only allows statuses of "Open", "In Progress", or "Complete"
    @app_commands.command(name='updatestatus', description='Update the status of a task')
    async def update_status(self, interaction: discord.Interaction, task_id: int, status: str):
        async with aiohttp.ClientSession() as session:
            if (status != "Open" and status != "In Progress" and status != "Completed"):
                await interaction.response.send_message(f"Invalid status. Please enter 'Open', 'In Progress', or 'Completed'.")
                return
            data = {'status': status}
            async with session.patch(f"http://localhost:8000/updatetask/{task_id}", json=data) as response:
                if response.status == 200:
                    await interaction.response.send_message(f"Task #{task_id} status updated to {status}!")
                else:
                    await interaction.response.send_message(f"Error updating task status.")
                    print(await response.text())

    # /deletetask <task_id>
    @app_commands.command(name='deletetask', description='Delete a task')
    async def delete_task(self, interaction: discord.Interaction, task_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"http://localhost:8000/deletetask/{task_id}") as response:
                if response.status == 200:
                    await interaction.response.send_message(f"Task #{task_id} deleted successfully!")
                else:
                    await interaction.response.send_message(f"Error deleting task.")
                    print(await response.text())


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await bot.add_cog(TaskCommands(bot))
    synced_commands = await tree.sync()
    print(f'Synced {len(synced_commands)} commands with Discord.')
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

# Load environment variables and run the bot
load_dotenv()
token = os.getenv('TOKEN')

try:
    bot.run(token)  # Token located in .env file as "TOKEN"
except Exception as e:
    print(f"Error starting bot: {e}")  # Print any errors that occur during bot startup
