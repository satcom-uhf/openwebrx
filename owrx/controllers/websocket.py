from . import Controller
from owrx.websocket import WebSocketConnection
from owrx.connection import HandshakeMessageHandler
import logging
import os
from .utils import HashCheck
logger = logging.getLogger(__name__)

class WebSocketController(Controller):
    def indexAction(self):
        secret = os.environ['BOT_TOKEN'].encode('utf-8')
        logger.debug(self.request.query)
        if not HashCheck(self.request.query, secret).check_hash():
            self.send_response("Unauthorized", 403, "application/json")
        else:
            conn = WebSocketConnection(self.handler, HandshakeMessageHandler())
            conn.handle()
