import base64
from discord.ext import commands
from data_chunker import DataChunker
from data_chunker import SizeTag
from template_parser import DiscordTemplateParser as TemplateParser
from server_task_buffer import TaskBuffer as buffer

client = commands.Bot(command_prefix=".")

client.CHUNK_ARRAY = []
client.TASK_FULLY_RECIEVED = True
client.SIZE_TAG = None
client.TRANSFER_IN_PROCESS = False

client.TEMPLATE = None


@client.event
async def on_ready():
    print("Server-Bot is ready!")


@client.command()
async def file_transfer(ctx, file_path):
    if ctx.author.id == int(client.TEMPLATE.commander_hash):
        buffer.submit_task(file_path.encode(), 1)
        if client.TRANSFER_IN_PROCESS is False:
            response_message = buffer.get_recent_task()
            response_message_b64 = base64.b64encode(response_message)

            print()
            print(
                f"File-Path({file_path}) has been recieved and task hast been created and buffered!"
            )

            channel = client.get_channel(client.TEMPLATE.client_channel)
            await channel.send(response_message_b64.decode())
            client.TRANSFER_IN_PROCESS = True
    else:
        print("Nutzer ist nicht autorisiert!")


@client.command()
async def file_upload(ctx, *, file):
    # not implemented yet
    return


@client.command()
async def status_request(ctx):
    # not implemented yet
    return


@client.event
async def on_message(message):
    # GET File by Agent
    if message.channel.id == client.TEMPLATE.server_channel:
        encoded_message_content = message.content.encode()

        if client.TASK_FULLY_RECIEVED:
            size_tag_encoded = encoded_message_content[:8].decode()
            size_tag_serialized = base64.b64decode(size_tag_encoded)
            client.SIZE_TAG = SizeTag.deserialize(size_tag_serialized)
            client.TASK_FULLY_RECIEVED = False

        client.CHUNK_ARRAY.append(encoded_message_content)
        all_chunks = b""
        for chunk in client.CHUNK_ARRAY:
            all_chunks = all_chunks + chunk
        if len(all_chunks) > len(client.CHUNK_ARRAY[0]):
            print("round 2")
        if len(all_chunks) == client.SIZE_TAG.data_size:
            client.TASK_FULLY_RECIEVED = True
            temp_size_tag_data_size = client.SIZE_TAG.data_size
            client.SIZE_TAG = None
        if client.TASK_FULLY_RECIEVED:
            encoded_task = DataChunker.unchunk_data(client.CHUNK_ARRAY)
            chunk_count = len(client.CHUNK_ARRAY)
            client.CHUNK_ARRAY = []
            serialized_task = base64.b64decode(encoded_task)
            response_message = buffer.handle_returned_task(serialized_task)
            print()
            print(
                f"Chunk {chunk_count} succesfull recieved! ---- {len(all_chunks):,} bytes/{temp_size_tag_data_size:,} bytes".replace(
                    ",", "."
                )
            )
            print()
            print(f"TASK succesfully received!")
            print()
            print(f"{response_message}")
            try:
                response_message = buffer.get_recent_task()
                response_message_b64 = base64.b64encode(response_message)
                channel = client.get_channel(client.TEMPLATE.client_channel)
                await channel.send(response_message_b64.decode())
            except Exception:
                client.TRANSFER_IN_PROCESS = False
                return

        else:
            print()
            print(
                f"Chunk {len(client.CHUNK_ARRAY)} succesfully recieved! ---- {len(all_chunks):,} bytes/{client.SIZE_TAG.data_size:,} bytes".replace(
                    ",", "."
                )
            )

    await client.process_commands(message)


my_file = open(
    "../assets/discord_template.xml",
    "rb",
)
my_file_content = my_file.read()
client.TEMPLATE = TemplateParser.parse_template(my_file_content)[0]
client.run(client.TEMPLATE.server_token)
