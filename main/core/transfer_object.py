from base64 import b64encode
from struct import calcsize, pack, unpack
from random import randint

from black import InvalidInput


class SizeTag:
    SIZE_TAG_SIZE = 8

    def __init__(self, data_size):
        self.data_size = data_size

    def serialize(self):
        return pack("i", self.data_size)

    def deserialize(serialized_size_tag):
        i = calcsize("i")
        (data_size,) = unpack("i", serialized_size_tag[0:i])
        return SizeTag(data_size=data_size)


class Marker:
    MARKER_SIZE = 12

    def __init__(self, end_of_payload=0, next_marker=0):
        self.end_of_payload = end_of_payload
        self.next_marker = next_marker

    def serialize(self):
        return pack("ii", self.end_of_payload, self.next_marker)

    def deserialize(serialized_marker):
        size = calcsize("ii")
        (end_of_payload, next_marker) = unpack("ii", serialized_marker[0:size])
        return Marker(end_of_payload=end_of_payload, next_marker=next_marker)


class SubChunk:
    MIN_SUBCHUNK_SIZE = 24

    def __init__(self, size, marker=None, payload=None, dummy=None):
        if size >= self.MIN_SUBCHUNK_SIZE:
            self.size = size
        else:
            raise ValueError(
                f"SubChunk muss mindestens {self.MIN_SUBCHUNK_SIZE} Zeichen groß sein!"
            )
        self.marker = marker
        self.payload = payload
        self.dummy = dummy

    def serialize(self):
        return b64encode(self.marker.serialize()) + self.payload + self.dummy


class Chunk:
    MIN_CHUNK_SIZE = 100 - SizeTag.SIZE_TAG_SIZE

    def __init__(self, size, subchunks_to_set=None):
        if size >= self.MIN_CHUNK_SIZE:
            self.size = size
        else:
            raise ValueError(
                f"Chunk muss mindestns {self.MIN_CHUNK_SIZE} Zeichen groß sein!"
            )
        self.subchunks = subchunks_to_set

    def serialize(self):
        byte = b""
        for subchunk in self.subchunks:
            byte = byte + subchunk.serialize()
        return byte

    def sub_chunking(self, payload_percentage, message):
        if len(message) == 0:
            raise ValueError(f"'message' darf nicht 0 sein!")
        # setze Methoden Variable
        rest_chunk_size = self.size

        # SUBCHUNKING-START
        while rest_chunk_size > 0:
            subchunk_size = randint(SubChunk.MIN_SUBCHUNK_SIZE, rest_chunk_size)
            # bleibt genug übrig um danach einen weiteren SubChunk zu bilden?
            if (
                rest_chunk_size - subchunk_size < SubChunk.MIN_SUBCHUNK_SIZE
                or len(message) == 0
            ):
                subchunk_size = rest_chunk_size

            rest_chunk_size = rest_chunk_size - subchunk_size

            subchunk = SubChunk(size=subchunk_size)
            subchunk_size = subchunk_size - Marker.MARKER_SIZE
            if len(message) == 0:
                subchunk.dummy = DummyGenerator.get_dummy_data(subchunk_size)
                subchunk.marker = Marker(next_marker=subchunk.size)
                self.subchunks.append(
                    SubChunk(
                        size=subchunk.size,
                        marker=subchunk.marker,
                        payload=b"",
                        dummy=subchunk.dummy,
                    )
                )
                break
            if len(message) < int(
                (subchunk_size - Marker.MARKER_SIZE) * payload_percentage
            ):
                # letzter SubChunk
                subchunk.payload = message
                message = ""
            else:
                subchunk.payload = message[: int(subchunk_size * payload_percentage)]
                message = message[int(subchunk_size * payload_percentage) :]
            subchunk.dummy = DummyGenerator.get_dummy_data(
                subchunk_size - len(subchunk.payload)
            )
            subchunk.marker = Marker(
                end_of_payload=len(subchunk.payload),
                next_marker=subchunk.size - Marker.MARKER_SIZE,
            )
            if self.subchunks is None:
                self.subchunks = []

            self.subchunks.append(
                SubChunk(
                    size=subchunk.size,
                    marker=subchunk.marker,
                    payload=subchunk.payload,
                    dummy=subchunk.dummy,
                )
            )
            del subchunk
        # SUBCHUNKING-ENDE

        # gebe Rest der Message zurück
        return message


class TransferObject:
    def __init__(self, message, size_tag=None, chunks=None):
        self.message = message
        self.size_tag = size_tag
        self.chunks = chunks

    def serialize(self):
        array = []
        for chunk in self.chunks:
            if len(array) == 0:
                byte = b64encode(self.size_tag.serialize()) + chunk.serialize()
            else:
                byte = chunk.serialize()
            array.append(byte)
        return array

    def chunking(self, payload_percentage, chunk_size_range):
        # setze Methoden Variable
        temp_message = self.message
        self.chunks = []
        first = True
        while len(temp_message) > 0:
            if first:
                if (
                    chunk_size_range.stop - SizeTag.SIZE_TAG_SIZE
                    >= chunk_size_range.start
                ):
                    chunk = Chunk(
                        size=randint(
                            chunk_size_range.start,
                            chunk_size_range.stop - SizeTag.SIZE_TAG_SIZE,
                        )
                    )
                else:
                    chunk = Chunk(size=chunk_size_range.stop - SizeTag.SIZE_TAG_SIZE)
                first = False
            else:
                chunk = Chunk(
                    size=randint(chunk_size_range.start, chunk_size_range.stop)
                )
            temp_message = chunk.sub_chunking(
                payload_percentage=payload_percentage, message=temp_message
            )
            self.chunks.append(Chunk(size=chunk.size, subchunks_to_set=chunk.subchunks))
            for subchunk in chunk.subchunks:
                del subchunk
            del chunk.subchunks
            del chunk


class DummyGenerator:
    WORDS = [
        "Hallo",
        "Welt",
        "Wie",
        "Gehts",
        "Schoen",
        "Haesslich",
        "Leben",
        "Ist",
        "Butter",
        "Birne",
        "Abfall",
        "Kopf",
        "Rofl",
        "Jumks",
        "Und",
        "Auch",
    ]

    def get_dummy_data(size):
        i = 0
        random_string = ""
        while len(random_string) < size:
            i = randint(0, len(DummyGenerator.WORDS) - 1)
            random_string = random_string + DummyGenerator.WORDS[i]

        return random_string[:size].encode()
