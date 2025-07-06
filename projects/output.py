import os
from twilio.rest import Client

def send_sms(to_number, body):
    """
    Sends an SMS message via Twilio.

    Args:
        to_number (str): The recipient's phone number (e.g., "+1234567890").
        body (str): The message body.
    """
    # Your Account SID and Auth Token from twilio.com/console
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, twilio_phone_number]):
        print("Error: Twilio credentials (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER) not set as environment variables.")
        return

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            to=to_number,
            from_=twilio_phone_number,
            body=body
        )
        print(f"Message SID: {message.sid}")
        print(f"Message status: {message.status}")
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == "__main__":
    # Example usage:
    # Make sure to set the following environment variables:
    # TWILIO_ACCOUNT_SID
    # TWILIO_AUTH_TOKEN
    # TWILIO_PHONE_NUMBER

    # Replace with the actual recipient number and message
    # recipient_number = "+15551234567"
    # message_body = "Hello from your Python Twilio SMS sender!"
    # send_sms(recipient_number, message_body)