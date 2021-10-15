from . import Controller
from owrx.websocket import WebSocketConnection
from owrx.connection import HandshakeMessageHandler
import logging

logger = logging.getLogger(__name__)

class WebSocketController(Controller):
    def indexAction(self):
        logger.debug("WEBSOOOKETTTT")
        logger.debug(self.request.query)
        conn = WebSocketConnection(self.handler, HandshakeMessageHandler())
        # enter read loop
        conn.handle()
