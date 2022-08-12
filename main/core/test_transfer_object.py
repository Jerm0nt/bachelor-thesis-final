import unittest

from transfer_object import *


class TransferObjectTest(unittest.TestCase):
    def test_chunk_good_1(self):
        print()
        print("#1 Chunks Good Test")
        index = 200
        while index < 1000:
            chunk = Chunk(size=index)
            test = "test"
            while len(test) < 10000:
                test = test + "test"
            test_back = chunk.sub_chunking(0.5, test.encode())
            self.assertTrue(len(test_back) < len(test.encode()))
            self.assertTrue(len(chunk.serialize()) == chunk.size == index)
            index = index + 1

    def test_chunk_good_short_message_2(self):
        print()
        print("#2 Chunk Good Test - short message")
        index = 200
        while index < 2000:
            chunk = Chunk(size=index)
            test = "t"
            test_back = chunk.sub_chunking(0.5, test.encode())
            self.assertTrue(len(test_back) < len(test.encode()))
            if not len(chunk.serialize()) == chunk.size:
                print(
                    f"len(chunk.serialize)  = {len(chunk.serialize())}; chunk.size = {chunk.size}"
                )
            self.assertTrue(len(chunk.serialize()) == chunk.size == index)
            index = index + 1

    def test_chunk_good_long_message_3(self):
        print()
        print("#3 Chunk Good Test - long message")
        index = 200
        while index < 2000:
            chunk = Chunk(size=index)
            test = "test"
            while len(test) < 50000:
                test = test + "test"
            test_back = chunk.sub_chunking(0.5, test.encode())
            self.assertTrue(len(test_back) < len(test.encode()))
            if not len(chunk.serialize()) == chunk.size:
                print(
                    f"len(chunk.serialize)  = {len(chunk.serialize())}; chunk.size = {chunk.size}"
                )
            self.assertTrue(len(chunk.serialize()) == chunk.size == index)
            index = index + 1

    def test_chunk_size_too_low_4(self):
        print()
        print("#4 Chunk Test - size too low")
        with self.assertRaises(ValueError):
            Chunk(size=Chunk.MIN_CHUNK_SIZE - 1)

    def test_chunk_message_empty_5(self):
        print()
        print("#5 Chunk Test - message empty")
        index = 200
        chunk = Chunk(size=index)
        test = ""
        with self.assertRaises(ValueError):
            chunk.sub_chunking(0.5, test.encode())
            index = index + 1

    def test_transfer_object_good_6(self):
        print()
        print("#6 TransferObject Good Test")
        i = Chunk.MIN_CHUNK_SIZE + SizeTag.SIZE_TAG_SIZE
        while i < 1000:
            test = "Test"
            while len(test) < 500:
                test = test + "Test"
            transfer_object = TransferObject(test.encode())
            transfer_object.chunking(0.5, range(i, i))
            array_index = 0
            for chunk in transfer_object.chunks:
                if array_index == 0:
                    self.assertTrue(len(chunk.serialize()) == i - SizeTag.SIZE_TAG_SIZE)
                else:
                    self.assertTrue(i <= len(chunk.serialize()) <= i)
                    self.assertTrue(chunk.size == len(chunk.serialize()) == i)
                array_index = array_index + 1
            i = i + 1

    def test_transfer_object_bad_range_input_7(self):
        print()
        print("#7 TransferObject Test - Bad Range Input")
        test = "Test"
        while len(test) < 500:
            test = test + "Test"
        transfer_object = TransferObject(test.encode())
        with self.assertRaises(ValueError):
            transfer_object.chunking(
                0.5, range(Chunk.MIN_CHUNK_SIZE + 10, Chunk.MIN_CHUNK_SIZE + 1)
            )

    def test_transfer_object_good_8(self):
        print()
        print("#8 TransferObject Good Test - Range Test 500-700:500-701")
        test = "Test"
        while len(test) < 500:
            test = test + "Test"

        i = 500
        while i < 700:
            j = i
            while j < 701:
                transfer_object = TransferObject(test.encode())
                transfer_object.chunking(0.5, range(i, j))
                array_index = 0
                for chunk in transfer_object.chunks:
                    if array_index == 0:
                        self.assertTrue(
                            len(chunk.serialize()) + SizeTag.SIZE_TAG_SIZE <= j
                            or len(chunk.serialize()) >= i
                        )
                    else:
                        self.assertTrue(i <= len(chunk.serialize()) <= j)
                        self.assertTrue(chunk.size == len(chunk.serialize()))
                j = j + 1
            i = i + 1

    def test_transfer_object_good_9(self):
        print()
        print("#9 TransferObject Good Test - 1000 max")

        string_to_transfer = "Test"
        for i in range(1000):
            string_to_transfer = string_to_transfer + "Test"

        index = 1
        while index < 1000:
            transfer_object = TransferObject(string_to_transfer.encode())
            transfer_object.chunking(0.5, range(990, 1000))
            chunks_index = 0
            for chunk in transfer_object.chunks:
                if len(chunk.serialize()) > 1000:
                    print(
                        f"Länge = : {len(chunk.serialize())}; {chunks_index} / {len(transfer_object.chunks)}"
                    )
                self.assertTrue(990 <= len(chunk.serialize()) <= 1000)
                chunks_index = chunks_index + 1
            index = index + 1


    def test_chunk_percentage_test_10(self):
        print()
        print("#11 Chunk Good Test - percentage")
        test = "test"
        while len(test) < 1000:
            test = test + "test"
        index = 0.05
        while index < 0.95:
            
            chunk = Chunk(size=1000)
            test_back = chunk.sub_chunking(index, test.encode())
            self.assertTrue(len(test_back) < len(test))
            for sub_chunk in chunk.subchunks:
                test_sc = sub_chunk.payload + sub_chunk.dummy   
                """print(f"index: {index}")  
                print(f"len(sub_chunk.payload): {len(sub_chunk.payload)}")
                print(f"len(test_sc) * index: {len(test_sc) * index}")
                print()"""
                self.assertAlmostEqual(len(sub_chunk.payload), len(test_sc) * index, delta=1.0)
            index = index + 0.05


if __name__ == "__main__":
    print()
    print("##### TransferObject-Test ######")
    unittest.main()
