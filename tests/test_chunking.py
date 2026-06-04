import unittest

from app.pipeline.chunking import split_text_into_chunks


class ChunkingTests(unittest.TestCase):
    def test_split_text_into_chunks_uses_overlap(self):
        words = [f"w{i}" for i in range(1, 501)]
        text = " ".join(words)

        chunks = split_text_into_chunks(text, max_words=200)

        self.assertGreaterEqual(len(chunks), 3)

        first_chunk_words = chunks[0].split()
        second_chunk_words = chunks[1].split()

        self.assertEqual(first_chunk_words[-60:], second_chunk_words[:60])


if __name__ == "__main__":
    unittest.main()
