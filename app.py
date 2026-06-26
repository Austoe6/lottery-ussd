"""
LuckyDraw USSD lottery - Africa's Talking callback server.

Docs:
  https://developers.africastalking.com/docs/authentication
  https://developers.africastalking.com/docs/ussd/overview
  https://developers.africastalking.com/docs/ussd/handle_sessions
  https://developers.africastalking.com/docs/ussd/notifications
"""

import logging
import os

from flask import Flask, make_response, request

from ussd_handler import handle_ussd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def _plain_response(body: str, status: int = 200):
    resp = make_response(body, status)
    resp.headers["Content-Type"] = "text/plain"
    return resp


@app.route("/ussd", methods=["POST"])
@app.route("/api/ussd/callback", methods=["POST"])
def ussd_callback():
    """
    Africa's Talking USSD webhook.

    POST fields: sessionId, serviceCode, phoneNumber, networkCode, text
    Responses must start with CON (continue) or END (terminate).
    """
    session_id = request.values.get("sessionId", "")
    service_code = request.values.get("serviceCode", "")
    phone_number = request.values.get("phoneNumber", "")
    text = request.values.get("text", "")

    logger.info(
        "USSD session=%s phone=%s service=%s text=%r",
        session_id,
        phone_number,
        service_code,
        text,
    )

    try:
        menu = handle_ussd(text, phone_number)
    except Exception:
        logger.exception("USSD handler error session=%s", session_id)
        menu = "END Service temporarily unavailable. Please try again."

    if not menu.startswith(("CON ", "CON\n", "END ", "END\n")):
        logger.error("Malformed USSD response: %r", menu)
        menu = "END Service error. Please try again."

    return _plain_response(menu)


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "luckydraw-ussd"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
