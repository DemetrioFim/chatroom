import unittest
import requests
from app.chatbot import get_stock

class MainTest(unittest.TestCase):
    def test_get(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(200, response.status_code)

    def test_index(self):
        response = requests.get('http://127.0.0.1:5000/index')
        self.assertEqual(200, response.status_code)

    def test_login(self):
        response = requests.get('http://127.0.0.1:5000/login')
        self.assertEqual(200, response.status_code)

    def test_content_type(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertIn('text/javascript', response.text)

    def test_good_chatbot(self):
        share = 'aapl.us'
        msg = f'/stock={share.lower()}'
        good_test = get_stock(msg)
        self.assertIn(f"{share.upper()} quote is $", good_test)

    def test_bad_chatbod(self):
        share = 'appl.us'
        msg = f'/stock={share.lower()}'
        bad_test = get_stock(msg)
        self.assertEqual("Share not found!", bad_test)

if __name__ == '__main__':
    unittest.main()
