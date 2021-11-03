from typing import Any
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

class FirebaseNotifications:
    def __init__(self, config_path: str = None) -> None:
        self.agent = 'firebase'
        self.config_path = config_path
    
    def initialize(self):
        cred = credentials.Certificate(self.config_path)
        firebase_admin.initialize_app(cred)
        
        return self
    
    def send_to_token(self, destination: str, title: str, body: str, image_url: str = '', data: Any = None) -> 'FirebaseNotifications':
        message = messaging.Message(
            token=destination,
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image_url
            )
        )
        if data is not None:
            message.data = data

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return self
    
    def send_to_topic(self, topic: str, title: str, body: str, image_url: str = '', data: Any = None) -> 'FirebaseNotifications':
        message = messaging.Message(
            topic=topic,
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image_url
            )
        )
        if data is not None:
            message.data = data

        # Send a message to the device corresponding to the provided
        # registration token.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return self