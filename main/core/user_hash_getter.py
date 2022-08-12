import discord
from template_parser import DiscordTemplateParser as TemplateParser

client = discord.Client()

client.TEMPLATE = None


@client.event
async def on_message(message):
    print(message.author.avatar)


my_file = open(
    "../assets/discord_template.xml",
    "rb",
)
my_file_content = my_file.read()
client.TEMPLATE = TemplateParser.parse_template(my_file_content)[0]
client.run(client.TEMPLATE.server_token)
