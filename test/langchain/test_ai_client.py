import unittest

from app.core.ai_client import generate_ai_client, get_chain
from app.utils.chess_util import init_game


class AIClientTest(unittest.TestCase):
    def test_generate_ai_client(self):
        client = generate_ai_client()
        print('generated')
        self.assertIsNotNone(client)
        print('send_message')
        received_message = client.invoke("plz print 'hello world'")
        print("received_message : " + received_message.content)
        self.assertIsNotNone(received_message)

    def test_chass_response(self):
        board = init_game()
        client = get_chain()
        print('generated')
        response = client.invoke({
            "ai_role": "white",
            "moves": [],
            "user_move": None,
            "fen": board.fen()
        })
        print(response)
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
