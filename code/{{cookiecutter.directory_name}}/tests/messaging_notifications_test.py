import unittest
import os

from api.utils.notifications import MessagingNotification

from dotenv import load_dotenv
load_dotenv('test.env')

class TestApi(unittest.TestCase):

    def test_firebase_notification(self):
        user_token = os.environ['USER_TOKEN']
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../', os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
        try:
            MessagingNotification('firebase').initialize(config_path).to_one(user_token, "Example", "Body example of notification")
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(True)

