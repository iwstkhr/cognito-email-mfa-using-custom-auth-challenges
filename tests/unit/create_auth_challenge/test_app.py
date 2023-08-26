from pytest_mock import MockerFixture

from create_auth_challenge import app


def test_lambda_handler_1():
    """ When CUSTOM_CHALLENGE """

    event = {
        'request': {
            'session': [
                {'challengeName': 'CUSTOM_CHALLENGE', 'challengeResult': True, 'challengeMetadata': 'challenge-123456'},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'privateChallengeParameters': {'answer': '123456'},
            'challengeMetadata': 'challenge-123456',
        }
    }


def test_lambda_handler_2(mocker: MockerFixture):
    """ WHEN NOT CUSTOM_CHALLENGE """

    mocker.patch('create_auth_challenge.app.generate_code', return_value='123456')
    mocker.patch('create_auth_challenge.app.create_message', return_value='message')
    mocker.patch('create_auth_challenge.app.send_mail_to')

    event = {
        'request': {
            'session': [
                {'challengeName': 'PASSWORD_VERIFIER', 'challengeResult': True},
            ],
            'userAttributes': {'email': 'abc@xyz.com'}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    app.send_mail_to.assert_called_once_with(
        event['request']['userAttributes']['email'],
        app.create_message.return_value
    )
    assert result == {
        'request': event['request'],
        'response': {
            'privateChallengeParameters': {'answer': '123456'},
            'challengeMetadata': 'challenge-123456',
        }
    }


def test_generate_code():
    assert len(app.generate_code(10)) == 10


def test_create_message():
    assert app.create_message('123456') == 'Your authentication code: 123456'


def test_send_mail_to(mocker: MockerFixture):
    mocker.patch('create_auth_challenge.app.client')
    mocker.patch('create_auth_challenge.app.EMAIL_SENDER', 'source@xyz.com')
    app.send_mail_to('abc@xyz.com', 'body')
    app.client.send_email.assert_called_once_with(
        Source='source@xyz.com',
        Destination={
            'ToAddresses': ['abc@xyz.com'],
        },
        Message={
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Authentication Code',
            },
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'body',
                },
            },
        }
    )
