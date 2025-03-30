import unittest

from app.core.ai_client import generate_ai_client


class AIClientTest(unittest.TestCase):
    def test_generate_ai_client(self):
        client = generate_ai_client()
        print('generated')
        self.assertIsNotNone(client)
        print('send_message')
        received_message = client.invoke("plz print 'hello world'")
        print("received_message : " + received_message.content)
        self.assertIsNotNone(received_message)

if __name__ == '__main__':
    unittest.main()
