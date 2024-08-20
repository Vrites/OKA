import os
from discord import Intents, Client, Message
import re
import pandas as pd
import webserver

DISCORD_TOKEN = os.environ["discordkey"]

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

@client.event
async def on_ready() -> None:
	print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
	username: str = str(message.author)
	user_message: str = message.content
	channel: str = str(message.channel)

	print(f'[{channel}] {username}: "{user_message}"')
	if message.author == client.user:
		return
	if message.channel.name == "general":
		if "https://www.raidbots.com" in message.content:
			m = re.match("^(?:[^\/]*\/){5}(.*)",message.content)
			data = "https://www.raidbots.com/reports/"+m.group(1)+"/data.csv"
			r = pd.read_csv("links.csv")
			csvData = {
				'name': message.author.name,
				'link': data,
				'entry': r.index + 1
			}
			if(r == message.author.name).any().any():
				print("we in if")
				r.loc[r["name"] == message.author.name, "link"] = data
			else:
				print("we went else")
				df = pd.DataFrame(csvData)
				df.to_csv("links.csv", mode="a", index=False, header=False)
		await message.delete()

webserver.keep_alive()

def main() -> None:
	client.run(token=DISCORD_TOKEN)

if __name__ == "__main__":
	main()
