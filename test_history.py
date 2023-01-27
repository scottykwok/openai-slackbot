import unittest
from history import ConversationHistory

class TestConversationHistory(unittest.TestCase):
    def setUp(self):
        self.history = ConversationHistory()

    def test_appendHistory(self):
        self.history.appendMessage(1, "Hello")
        self.assertEqual(self.history.ts_to_history[1], ["Hello"])

        self.history.appendMessage(1, "World")
        self.assertEqual(self.history.ts_to_history[1], ["Hello", "World"])

    def test_retrieveHistory(self):
        self.history.appendMessage(1, "Hello")
        self.history.appendMessage(1, "World")
        self.assertEqual(
            self.history.retrieveMessages(1, 15), ["Hello", "World"]
        )
        self.assertEqual(
            self.history.retrieveMessages(1, 5), [ "World"]
        )

if __name__ == "__main__":
    unittest.main()
