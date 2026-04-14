import unittest
import numpy as np
from src.embeddings.embedder import embed_texts

class TestEmbedder(unittest.TestCase):
    def test_empty_input_returns_empty(self):
        result = embed_texts([])
        self.assertEqual(result, [])
    
    def test_output_length_matches_input(self):
        texts = ["hello", "world", "foo", "bar", "baz qux"]
        result = embed_texts(texts)
        self.assertEqual(len(result), len(texts))
    
    def test_vector_dimension_is_correct(self):
        result = embed_texts(["any text here"])
        self.assertEqual(len(result[0]), 384)
    
    def test_output_contains_floats(self):
        result = embed_texts(["test"])
        self.assertTrue(all(isinstance(v, float) for v in result[0]))

    def test_similar_texts_are_closer_than_different(self):
        similar_a = "how does the login work"
        similar_b = "how is the authentication handled"
        different = "what is the weather today"

        vecs = embed_texts([similar_a, similar_b, different])

        def cosine_similarity(a, b):
            a, b = np.array(a), np.array(b)
            return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        sim_similar = cosine_similarity(vecs[0], vecs[1])
        sim_different = cosine_similarity(vecs[0], vecs[2])

        self.assertGreater(sim_similar, sim_different)
    
    def test_same_text_produces_same_vector(self):
        text = "def authenticate(user): pass"
        self.assertEqual(embed_texts([text]), embed_texts([text]))
