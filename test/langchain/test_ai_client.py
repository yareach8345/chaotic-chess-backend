import unittest

from app.core.ai_client import generate_ai_client, get_chain
from app.utils.chess_util import init_game


class AIClientTest(unittest.TestCase):
    def test_generate_ai_client(self):
        client = generate_ai_client()
        self.assertIsNotNone(client)
        received_message = client.invoke("plz print 'hello world'")
        self.assertIsNotNone(received_message)

    def test_chass_response(self):
        board = init_game()
        client = get_chain()
        response = client.invoke({
            "ai_role": "white",
            "moves": [],
            "user_move": None,
            "fen": board.fen()
        })
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
