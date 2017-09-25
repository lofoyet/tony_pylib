#! /usr/bin/python
# -*- encoding: utf-8 -*-
import os
import json
from slackclient import SlackClient


class SlackMessenger(object):
    """
    Used to send slack message
    """

    def __init__(self, token_path):
        auth = json.load(open(token_path, "rb"))
        self.token = auth["Token"]
        self.msger = SlackClient(self.token)
        self.me = auth["me"]
        self.business_group = auth["business_group_id"]
        self.reporting_run = auth["report_run"]

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
        self.send_message(text, self.business_group)

    def send_message_to_reporting_run(self, text):
        self.send_message(text, self.reporting_run)
