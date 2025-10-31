"""
Basic tests for the RAG Finance Tracking System.
"""

import sys
import unittest
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import RAGConfig, DocumentLoader, LocalEmbeddings


class TestConfiguration(unittest.TestCase):
    """Test configuration module."""
    
    def test_config_creation(self):
        """Test creating a configuration object."""
        config = RAGConfig()
        self.assertIsNotNone(config)
        self.assertEqual(config.chunk_size, 1000)
        self.assertEqual(config.chunk_overlap, 200)
        self.assertEqual(config.top_k, 4)
    
    def test_config_custom_values(self):
        """Test configuration with custom values."""
        config = RAGConfig(
            chunk_size=500,
            chunk_overlap=100,
            top_k=5
        )
        self.assertEqual(config.chunk_size, 500)
        self.assertEqual(config.chunk_overlap, 100)
        self.assertEqual(config.top_k, 5)


class TestDocumentLoader(unittest.TestCase):
    """Test document loader module."""
    
    def test_loader_creation(self):
        """Test creating a document loader."""
        loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
        self.assertIsNotNone(loader)
        self.assertEqual(loader.chunk_size, 1000)
        self.assertEqual(loader.chunk_overlap, 200)
    
    def test_load_text_file(self):
        """Test loading a text file."""
        # Create a temporary test file
        test_file = Path("/tmp/test_doc.txt")
        test_content = "This is a test document for RAG system. " * 50
        test_file.write_text(test_content)
        
        loader = DocumentLoader(chunk_size=100, chunk_overlap=20)
        documents = loader.load_text_file(test_file)
        
        self.assertGreater(len(documents), 0)
        self.assertTrue(all(doc.page_content for doc in documents))
        self.assertTrue(all("source" in doc.metadata for doc in documents))
        
        # Cleanup
        test_file.unlink()


class TestEmbeddings(unittest.TestCase):
    """Test embeddings module."""
    
    def test_embeddings_creation(self):
        """Test creating embeddings object."""
        # This test may take a while on first run as it downloads the model
        embeddings = LocalEmbeddings()
        self.assertIsNotNone(embeddings)
    
    def test_embed_query(self):
        """Test embedding a single query."""
        embeddings = LocalEmbeddings()
        query = "What is the revenue?"
        embedding = embeddings.embed_query(query)
        
        self.assertIsInstance(embedding, list)
        self.assertGreater(len(embedding), 0)
        self.assertTrue(all(isinstance(x, float) for x in embedding))
    
    def test_embed_documents(self):
        """Test embedding multiple documents."""
        embeddings = LocalEmbeddings()
        texts = [
            "Financial statement analysis",
            "Revenue and expenses",
            "Balance sheet overview"
        ]
        embeddings_list = embeddings.embed_documents(texts)
        
        self.assertEqual(len(embeddings_list), 3)
        self.assertTrue(all(isinstance(emb, list) for emb in embeddings_list))


if __name__ == "__main__":
    unittest.main()
