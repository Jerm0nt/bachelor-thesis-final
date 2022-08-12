import hashlib
from task import TaskingObject, TransferStatus, TransferType
import os
from time import time


class TaskBuffer:
    task_id_counter = 0
    tasks = []

    def get_task_id_counter():
        TaskBuffer.task_id_counter += 1
        return TaskBuffer.task_id_counter

    def get_recent_task():
        for tsk in TaskBuffer.tasks:
            if tsk.status == TransferStatus.QUEUED:
                tsk.status = TransferStatus.PENDING
                tsk_serialized = TaskingObject.serialize(tsk)
                return tsk_serialized
        raise Exception

    def delete_task(old_task):
        for task in TaskBuffer.tasks:
            if task.task_id == old_task.task_id:
                TaskBuffer.tasks.remove(task)
        return

    def submit_task(data, type):
        task = TaskingObject(
            data=data, task_id=TaskBuffer.get_task_id_counter(), type=type
        )
        TaskBuffer.tasks.append(task)
        return

    def handle_returned_task(serialized_task):
        task = TaskingObject.deserialize(serialized_task)

        if task.type == TransferType.FILE_TRANSFER.value:
            return TaskBuffer.file_transfer(task)

        elif task.type == TransferType.FILE_UPLOAD.value:
            return TaskBuffer.file_upload(task)

        elif task.type == TransferType.STATUS_REQUEST.value:
            return TaskBuffer.status_request(task)

    def file_transfer(task):
        response_message = ""
        try:
            decoded_data = task.data.decode()
        except Exception:
            decoded_data = 100
        if decoded_data == "-1":
            task.status = TransferStatus.FAILED
            response_message = "Operation failed! No such path!"
        else:
            md5Hashed = hashlib.md5(task.data).hexdigest()
            for tsk in TaskBuffer.tasks:
                if task.task_id == tsk.task_id:
                    tsk_data_string = tsk.data.decode()
                    file_name = os.path.basename(tsk_data_string)

            with open(f"../assets/recieved/{time()}_{file_name}", "wb") as binary_file:
                binary_file.write(task.data)
                binary_file.close()

            for tsk in TaskBuffer.tasks:
                if tsk.task_id == task.task_id:
                    tsk = task

            task.status = TransferStatus.SUCCESSFUL
            response_message = (
                f"File {md5Hashed} succesfully recieved! File saved as: {file_name}!"
            )
        TaskBuffer.delete_task(task)
        return response_message

    def file_upload(task):
        return "Not implemented yet!"

    def status_request(task):
        return "Not implemented yet!"
