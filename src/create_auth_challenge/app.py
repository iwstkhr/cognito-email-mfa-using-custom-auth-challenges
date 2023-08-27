# See https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html

import os
import random

import boto3

from layers.cognito_custom_challenge_helper import CustomChallengeRequest, CustomChallengeResponse

client = boto3.client('ses')

CODE_LENGTH = int(os.environ.get('CODE_LENGTH', 6))
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')


def lambda_handler(event: dict, context: dict) -> dict:
    # Parse the event to create a request object.
    request = CustomChallengeRequest(event)
    last_session = request.last_session

    if last_session.is_custom_challenge():
        # When the last session is a custom challenge, extract the otp code from the last session metadata.
        code = last_session.challenge_metadata.replace('challenge-', '')
    else:
        # When the last session is not a custom challenge, generate an otp code and send it to the client.
        code = generate_code()
        message = create_message(code)
        send_mail_to(request.user_attributes['email'], message)

    # Create a response
    response = CustomChallengeResponse(event)
    response.set_answer(code)
    response.set_metadata(f'challenge-{code}')
    event['response'] = response.__dict__()
    return event


def generate_code(length=CODE_LENGTH) -> str:
    return str(random.randint(0, 10 ** length - 1)).zfill(length)


def create_message(code: str) -> str:
    return f'Your authentication code: {code}'


def send_mail_to(email: str, body: str) -> None:
    client.send_email(
        Source=EMAIL_SENDER,
        Destination={
            'ToAddresses': [email],
        },
        Message={
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Authentication Code',
            },
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
        },
    )
