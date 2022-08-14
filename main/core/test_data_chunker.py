from base64 import b64decode, b64encode
import unittest
from data_chunker import DataChunker
from task import TaskingObject
from transfer_object import SizeTag


class DataChunkerTest(unittest.TestCase):
    def test_chunk_data_good_1(self):
        print()
        print("## Test 1 ##")
        test_index = 1
        while test_index < 100:
            min_chunk_size = 400
            max_chunk_size = 1000
            payload_percentage = 0.5

            string_to_transfer = "Test"
            for i in range(1000):
                string_to_transfer = string_to_transfer + "Test"

            data_chunker = DataChunker(
                max_chunk_size, min_chunk_size, payload_percentage
            )
            array = data_chunker.chunk_data(string_to_transfer.encode())
            index = 0
            for chunk in array:
                self.assertTrue(min_chunk_size <= len(chunk) <= max_chunk_size)
                index = index + 1
            test_index = test_index + 1

    def test_chunk_data_good_2(self):
        print()
        print("## Test 2 ##")
        test_index = 1
        while test_index < 100:
            min_chunk_size = 1000
            max_chunk_size = 5000
            payload_percentage = 0.5

            string_to_transfer = "Test"
            """
            for i in range(1000):
                string_to_transfer = string_to_transfer + "Test"
            """

            data_chunker = DataChunker(
                max_chunk_size, min_chunk_size, payload_percentage
            )
            array = data_chunker.chunk_data(string_to_transfer.encode())
            index = 0
            for chunk in array:
                if min_chunk_size > len(chunk) or len(chunk) > max_chunk_size:
                    print(f"Loop# {test_index}")
                    print(f"Array-Length: {len(array)}")
                    print(
                        f"#{index}: min_chunk_size = {min_chunk_size}; len(chunk) = {len(chunk)}; max_chunk_size = {max_chunk_size};"
                    )
                self.assertTrue(min_chunk_size <= len(chunk) <= max_chunk_size)
                index = index + 1
            test_index = test_index + 1

    def test_chunk_data_good_3(self):
        print()
        print("## Test 3 ##")
        test_index = 1
        while test_index < 100:
            min_chunk_size = 100
            max_chunk_size = 10000
            payload_percentage = 0.5

            string_to_transfer = "Test"
            for i in range(10000):
                string_to_transfer = string_to_transfer + "Test"

            data_chunker = DataChunker(
                max_chunk_size, min_chunk_size, payload_percentage
            )
            array = data_chunker.chunk_data(string_to_transfer.encode())
            index = 0
            for chunk in array:
                if min_chunk_size > len(chunk) or len(chunk) > max_chunk_size:
                    print(f"Loop # {test_index}")
                    print(f"Array-Length: {len(array)}")
                    print(
                        f"#{index}: min_chunk_size = {min_chunk_size}; len(chunk) = {len(chunk)}; max_chunk_size = {max_chunk_size};"
                    )
                self.assertTrue(min_chunk_size <= len(chunk) <= max_chunk_size)
                index = index + 1
            test_index = test_index + 1

    def test_chunk_data_good_percentage_4(self):
        print()
        print("## Test 4 ##")
        test_index = 0.05
        while test_index < 0.95:
            min_chunk_size = 400
            max_chunk_size = 1000
            payload_percentage = test_index

            string_to_transfer = "Test"
            for i in range(10000):
                string_to_transfer = string_to_transfer + "Test"

            data_chunker = DataChunker(
                max_chunk_size, min_chunk_size, payload_percentage
            )
            array = data_chunker.chunk_data(string_to_transfer.encode())
            index = 0
            for chunk in array:
                if min_chunk_size > len(chunk) or len(chunk) > max_chunk_size:
                    print(f"Loop # {test_index}")
                    print(f"Array-Length: {len(array)}")
                    print(
                        f"#{index}: min_chunk_size = {min_chunk_size}; len(chunk) = {len(chunk)}; max_chunk_size = {max_chunk_size};"
                    )
                self.assertTrue(min_chunk_size <= len(chunk) <= max_chunk_size)
                index = index + 1
            test_index = test_index + 0.05

    def test_integration_chunk_and_unchunk_data_5(self):
        print()
        print("## Test 5 ##")

        test = "Fischers fritze fischt frische Fische, frische Fische fischt Fischers fritze"

        while len(test) < 1000:
            test = test + test

        test_b64 = b64encode(test.encode())

        data_chunker = DataChunker(700, 500, 0.3)
        chunk_array = data_chunker.chunk_data(test_b64)

        test_back = DataChunker.unchunk_data(chunk_array)
        self.assertTrue(len(test) == len(b64decode(test_back).decode()))
        self.assertTrue(b64decode(test_back).decode() == test)

    def test_integration_chunk_and_unchunk_data_short_message_6(self):
        print()
        print("## Test 6 ##")

        test = "Fisc"

        test_b64 = b64encode(test.encode())

        data_chunker = DataChunker(700, 500, 0.3)
        chunk_array = data_chunker.chunk_data(test_b64)

        test_back = DataChunker.unchunk_data(chunk_array)
        self.assertTrue(len(test) == len(b64decode(test_back).decode()))
        self.assertTrue(b64decode(test_back).decode() == test)

    def test_integration_chunk_and_unchunk_data_7(self):
        print()
        print("## Test 7 ##")

        test = "Fischers fritze fischt frische Fische, frische Fische fischt Fischers fritze"

        while len(test) < 1000:
            test = test + test

        test_b64 = b64encode(test.encode())
        test_index_max = 200
        test_index_min = 100
        while test_index_max < 1000:
            data_chunker = DataChunker(test_index_max, test_index_min, 0.3)
            chunk_array = data_chunker.chunk_data(test_b64)

            test_back = DataChunker.unchunk_data(chunk_array)
            self.assertTrue(len(test) == len(b64decode(test_back).decode()))
            self.assertTrue(b64decode(test_back).decode() == test)
            test_index_max = test_index_max + 15
            test_index_min = test_index_min + 7

    def test_integration_chunk_length_8(self):
        print()
        print("## Test 8 ##")
        index = 1
        while index < 100:
            my_file = open("/Users/eblejerome/Downloads/Erklaerung.rtf", "rb")
            my_file_content = my_file.read()
            my_file.close()
            task = TaskingObject(type=0,task_id=1,data=my_file_content)

            data_chunker = DataChunker(
                max_chunk_size=2000,
                min_chunk_size=1900,
                payload_percentage=0.5,
            )

            serialized_task = TaskingObject.serialize(task)
            serialized_task_b64 = b64encode(serialized_task)

            post_array = data_chunker.chunk_data(serialized_task_b64)
            size_tag_encoded = post_array[0][:8].decode()
            size_tag_serialized = b64decode(size_tag_encoded)
            size_tag = SizeTag.deserialize(size_tag_serialized)

            all_chunks = b""

            for chunk in post_array:
                all_chunks = all_chunks + chunk

            self.assertEqual(len(all_chunks), size_tag.data_size)
            index = index + 1



if __name__ == "__main__":
    print()
    print("##### DataChunker-Test ######")
    unittest.main()


