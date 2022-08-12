import datetime
from enum import Enum
from struct import *


class TransferType(Enum):
    FILE_TRANSFER = 1
    FILE_UPLOAD = 2
    STATUS_REQUEST = 3


class TransferStatus(Enum):
    QUEUED = 0
    PENDING = 1
    SUCCESSFUL = 2
    FAILED = 3


class TaskingObject:
    UTF = "utf-8"

    def get_time_stamp():
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def __init__(self, type=0, task_id=0, data=""):
        self.type = int(type)
        self.task_id = task_id
        self.status = TransferStatus.QUEUED
        self.size = len(data)
        self.data = data
        self.creation_time = TaskingObject.get_time_stamp()
        self.sending_time = ""

    def __repr__(self):
        return f"Type : {str(self.type)},  ID: {str(self.task_id)}, Status: {str(self.status.value)}, Groeße: {str(self.size)}, Daten: {self.data.decode(TaskingObject.UTF)}, Creation Time: {self.creation_time}"

    def serialize(self):
        serialized_data = pack(
            "iiii", self.type, self.task_id, self.status.value, self.size
        )
        serialized_data += self.data
        return serialized_data

    def deserialize(serialized_data):
        i = calcsize("iiii")
        (type, task_id, status_value, size) = unpack("iiii", serialized_data[0:i])
        data = serialized_data[i:]
        task = TaskingObject(type=type, task_id=task_id, data=data)
        task.status = TransferStatus(status_value)
        return task
