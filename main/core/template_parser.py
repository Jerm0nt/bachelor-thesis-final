from abc import ABC, abstractmethod
from pipes import Template
import declxml as xml


class Template:
    def __init__(self, name, max_chunk_size, min_chunk_size, payload_percentage):
        self.name = name
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.payload_percentage = payload_percentage

        if min_chunk_size < 100:
            raise ValueError("Chunk-Size muss mindestens 100 sein.")

        if max_chunk_size < min_chunk_size:
            raise ValueError("Maximalgröße muss größer sein als Minimalgröße!")

        if payload_percentage < 0.05:
            raise ValueError("Payload Anteil muss mindestens 0.05 sein!")

        if payload_percentage > 1.0:
            raise ValueError("Payload Anteil kann höchstens 1.0 sein!")


class DiscordTemplate(Template):
    def __init__(
        self,
        name,
        max_chunk_size,
        min_chunk_size,
        payload_percentage,
        server_token,
        client_token,
        commander_hash,
        client_channel,
        server_channel,
    ):
        if max_chunk_size > 2000:
            raise ValueError(
                "Discord Nachrichten können maximal 2000 Zeichen lang sein."
            )
        super(DiscordTemplate, self).__init__(
            name, max_chunk_size, min_chunk_size, payload_percentage
        )
        self.server_token = server_token
        self.client_token = client_token
        self.commander_hash = commander_hash
        self.client_channel = client_channel
        self.server_channel = server_channel

    def __repr__(self):
        return f"{self.name} : \n max_chunk_size : {self.max_chunk_size}, \n min_chunk_size : {self.min_chunk_size}, \n payload_percentage : {self.payload_percentage}, \n server_token : {self.server_token}, \n commander_hash : {self.commander_hash}, \n client_channel : {self.client_channel}, \n server_channel : {self.server_channel}"


class TemplateParser(ABC):
    @abstractmethod
    def parse_template(template_content):
        pass


class DiscordTemplateParser(TemplateParser):
    def parse_template(template_content):
        processor = xml.array(
            xml.user_object(
                "DiscordTemplate",
                DiscordTemplate,
                [
                    xml.string("name"),
                    xml.integer("max-chunk-size", alias="max_chunk_size"),
                    xml.integer("min-chunk-size", alias="min_chunk_size"),
                    xml.floating_point(
                        "payload-percentage", alias="payload_percentage"
                    ),
                    xml.string("server-token", alias="server_token"),
                    xml.string("client-token", alias="client_token"),
                    xml.string("commander-hash", alias="commander_hash"),
                    xml.integer("client-channel", alias="client_channel"),
                    xml.integer("server-channel", alias="server_channel"),
                ],
            ),
            nested="Templates",
        )
        temp_entities = xml.parse_from_string(processor, template_content)
        return temp_entities


"""my_file = open(
    "main/assets/discord_template.xml",
    "rb",
)
my_file_content = my_file.read()
template_array = DiscordTemplateParser.parse_template(my_file_content)
template1 = template_array[0]

print(template1)"""
