from base64 import b64encode, b64decode
import random
from struct import *
from xml.dom import IndexSizeErr
from transfer_object import *


class DataChunker:

    def __init__(
        self,
        max_chunk_size=10000,
        min_chunk_size=500,
        payload_percentage=0.5,
    ):
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        self.payload_percentage = payload_percentage

    def chunk_data(self, chunkable_byte):
        transfer_object = TransferObject(message=chunkable_byte)
        transfer_object.chunking(
            payload_percentage=self.payload_percentage,
            chunk_size_range=range(self.min_chunk_size, self.max_chunk_size),
        )
        temp = None
        for chunk in transfer_object.chunks:
            if temp is None:
                temp = chunk.serialize()
            else:
                temp = temp + chunk.serialize()

        transfer_object.size_tag = SizeTag(data_size=len(temp) + SizeTag.SIZE_TAG_SIZE)
        return transfer_object.serialize()

    def unchunk_data(array):
        size_tag = None
        payload = None
        for array_chunk in array:
            if size_tag is None:
                size_tag = array_chunk[: SizeTag.SIZE_TAG_SIZE]
                array_chunk = array_chunk[SizeTag.SIZE_TAG_SIZE :]
            while len(array_chunk) > 0:
                marker = array_chunk[: Marker.MARKER_SIZE]
                marker = b64decode(marker)
                marker = Marker.deserialize(marker)
                array_chunk = array_chunk[Marker.MARKER_SIZE :]
                if payload is None:
                    payload = array_chunk[: marker.end_of_payload]
                else:
                    payload = payload + array_chunk[: marker.end_of_payload]
                array_chunk = array_chunk[marker.next_marker :]
        return payload

