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
        chatId = int(os.environ['CHAT_ID'])
        logger.debug(self.request.query)
        checker=HashCheck(self.request.query, secret)
        if not checker.check_hash():
            logger.warning("Wrong hash")
            self.send_response("Unauthorized", 401, "application/json")
        elif not checker.is_subscribed(chatId):
            logger.warning("Not subscribed")
            self.send_response("Unauthorized", 403, "application/json")
        else:
            conn = WebSocketConnection(self.handler, HandshakeMessageHandler())
            conn.handle()
