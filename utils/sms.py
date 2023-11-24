# This file will get replaced in the review step with real sms functionality.


import logging
from dataclasses import dataclass

@dataclass
class SMS:
    def __init__(self, phone_number: str, message: str):
        self.phone_number = phone_number
        self.message = message

    def send(self):
        logging.info(f'Sending {self.message} to {self.phone_number}')
