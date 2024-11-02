import os
import openai
import requests  # For weather API (if needed)
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  
print(WEATHER_API_KEY)

class Template(commands.Cog, name="template"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="testcommand",
        description="This command interacts with OpenAI to generate a response.",
    )
    async def testcommand(self, context: Context, *, user_input: str) -> None:
        """
        This command uses OpenAI to generate a response based on user input.

        :param context: The application command context.
        :param user_input: The input provided by the user for processing.
        """
        try:
            # Generate a response from OpenAI using the new method
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            # Extract the content of the response
            ai_response = response.choices[0].message.content

            # Send the AI response back to the Discord channel
            await context.send(ai_response)

        except Exception as e:
            # Handle errors (like API issues)
            await context.send(f"An error occurred: {str(e)}")

    @commands.hybrid_command(
        name="hello",
        description="Greet the user."
    )
    async def hello(self, context: Context) -> None:
        """Sends a greeting message."""
        await context.send("Hello! How can I assist you today?")

    @commands.hybrid_command(
        name="weather",
        description="Get the current weather for a specified city."
    )
    async def weather(self, context: Context, city: str) -> None:
        """Fetches and sends the current weather for the specified city."""
        try:
            # Example weather API URL - replace with actual API endpoint and parameters
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url).json()
            print(response)
            if response['cod'] != 200:
                await context.send("City not found. Please try again.")
                return

            temp = response['main']['temp']
            weather_description = response['weather'][0]['description']
            await context.send(f"The current weather in {city} is {temp}°C with {weather_description}.")
        
        except Exception as e:
            await context.send(f"An error occurred: {str(e)}")

    @commands.hybrid_command(
        name="remindme",
        description="Set a reminder for a specific time."
    )
    async def remindme(self, context: Context, time: str, *, reminder: str) -> None:
        """Sets a reminder."""
        # Note: You can implement a more complex reminder system using tasks.
        await context.send(f"Reminder set for {time}: {reminder}")

    @commands.hybrid_command(
        name="joke",
        description="Tell a random joke."
    )
    async def joke(self, context: Context) -> None:
        """Fetch and send a random joke."""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a joke"}
            ]
        )
        joke = response.choices[0].message.content
        await context.send(joke)

async def setup(bot) -> None:
    await bot.add_cog(Template(bot))
