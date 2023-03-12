import os
from typing import Any
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from .firebase import FirebaseNotifications

class NotInListException(Exception):
    AGENTS_LIST = ['firebase']
    def __init__(self, message: str=f"Notification agent not in list [{ ', '.join(AGENTS_LIST) }]") -> None:
        self.message = message
        super().__init__(self.message)


class MessagingNotification:
    def __init__(self, agent: str) -> None:
        self.agent = agent
    
    def initialize(self, config_path):
        if self.agent.lower() == 'firebase':
            self.firebase_not = FirebaseNotifications(config_path)
            self.firebase_not.initialize()
        
        else:
            raise NotInListException()
        
        return self
    
    def to_one(self, destination: str, title: str, body: str, image_url: str = '', data: Any = None) -> 'MessagingNotification':
        if self.agent == 'firebase':
            self.firebase_not.send_to_token(destination, title, body, image_url, data)
        else:
            raise NotInListException()
    
    def to_topic(self, topic: str, title: str, body: str, image_url: str = '', data: Any = None) -> 'MessagingNotification':
        if self.agent == 'firebase':
            self.firebase_not.send_to_topic(topic, title, body, image_url, data)
        else:
            raise NotInListException()