from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import gspread
from google.oauth2.service_account import Credentials

scopes = [
	"https://www.googleapis.com/auth/spreadsheets"
]

# These credentials you get from google cloud console
# I used this Youtube video to learn about everything sheets related in this file
# https://youtu.be/zCEJurLGFRk?si=0Jef3oUwsAknZ5Ax

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "YOUR_SPREADSHEET_ID"
workbook = client.open_by_key(sheet_id)

sheet = workbook.worksheet("YOUR_SPREADSHEET_NAME")

# Your bot token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# on_ready = stuff that happens once the bot is ready to do stuff
@client.event
async def on_ready() -> None:
	print(f'{client.user} is now running!')

  	#Everything below here is for my purposes

  	# Gets the channel that I intend to work with
	channel = client.get_channel(1275593586754322443)

  	# Gets the message history, since I'm not running this bot 24/7 and run it on my personal computer
	messages = channel.history(limit=200)
	if(messages):
    		# Loop the message history
		async for message in messages:
      			# Pass bots messages
			if message.author == client.user:
				pass
      			# If the message contains what I want
			if "https://www.raidbots.com" in message.content:
        			# Check if sheet contains the senders name already for updating
				cell = sheet.find(message.author.name)
        			# If it exists just edit the previous column of that row where it exists
				if(cell):
					sheet.update_cell(cell.row, cell.col-1, message.content)
        			# If it doesn't exist get the next empty row (definition below) and add data
				else:
					next_row = next_available_row(sheet)
					sheet.update_acell("A{}".format(next_row), message.content)
					sheet.update_acell("B{}".format(next_row), message.author.name)
      			# Delete message to keep channel clean, !! As this is inside the loop for message history, it iterates upto 200 messages in history and nukes them !!
      			# I use it but I've commented it for safety reasons if anyone happens to use this
			# await message.delete()

# When a message is sent this is run
@client.event
async def on_message(message: Message) -> None:
  	# Unnecessary bloat for logging
	username: str = str(message.author)
	user_message: str = message.content
	channel: str = str(message.channel)

	print(f'[{channel}] {username}: "{user_message}"')
  	# Pass if sender is bot
	if message.author == client.user:
		return
  	# Double check correct channel because message deleting is part of this
  	# All of this is also above, could be a function. I just didn't bother
	if message.channel.name == "olankylpyammesimit" and message.channel.id(1275593586754322443):
		if "https://www.raidbots.com" in message.content:
			cell = sheet.find(message.author.name)
			if(cell):
				sheet.update_cell(cell.row, cell.col-1, message.content)
			else:
				next_row = next_available_row(sheet)
				sheet.update_acell("A{}".format(next_row), message.content)
				sheet.update_acell("B{}".format(next_row), message.author.name)
		# Commented again for safety reasons
		# await message.delete()

# The function for the next free row
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

def main() -> None:
	client.run(token=TOKEN)

if __name__ == "__main__":
	main()
