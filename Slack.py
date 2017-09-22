#! /usr/bin/python
# -*- encoding: utf-8 -*-
import os
from slackclient import SlackClient


class SlackMessenger(object):
    """
    Used to send slack message
    """

    def __init__(self):
        self.token = "xoxp-2812264983-186712927904-242821448624-2af9518927db3d44bcede8a1ad54f616"
        self.msger = SlackClient(self.token)
        self.me = "@tony.liu"

    def send_message(self, text, to, as_me):
        if to == "me":
            to = self.me
        self.msger.api_call(
            "chat.postMessage",
            channel=to,
            text=text,
            as_user=as_me,
            # username="Cool guy",
        )

    def send_message_to_business_group(self, text):
        self.send_message(text, "G74EGDWFK")

    def send_message_to_reporting_run(self, text):
        self.send_message(text, "reporting_run")
