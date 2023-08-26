from define_auth_challenge import app
from layers.cognito_custom_challenge_helper import CustomChallengeName


def test_lambda_handler_1():
    """ When SRP_A """

    event = {
        'request': {
            'session': [
                {'challengeName': 'SRP_A', 'challengeResult': True},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'challengeName': CustomChallengeName.PASSWORD_VERIFIER.value,
            'issueTokens': False,
            'failAuthentication': False,
        },
    }


def test_lambda_handler_2():
    """ When PASSWORD_VERIFIER """

    event = {
        'request': {
            'session': [
                {'challengeName': 'PASSWORD_VERIFIER', 'challengeResult': True},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'challengeName': CustomChallengeName.CUSTOM_CHALLENGE.value,
            'issueTokens': False,
            'failAuthentication': False,
        },
    }


def test_lambda_handler_3():
    """ When CUSTOM_CHALLENGE and can issue tokens """

    event = {
        'request': {
            'session': [
                {'challengeName': 'CUSTOM_CHALLENGE', 'challengeResult': True},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'challengeName': '',
            'issueTokens': True,
            'failAuthentication': False,
        },
    }


def test_lambda_handler_4():
    """ When CUSTOM_CHALLENGE and cannot issue tokens """

    event = {
        'request': {
            'session': [
                {'challengeName': 'CUSTOM_CHALLENGE', 'challengeResult': False},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'challengeName': 'CUSTOM_CHALLENGE',
            'issueTokens': False,
            'failAuthentication': False,
        },
    }


def test_lambda_handler_5():
    """ When invalid request """

    event = {
        'request': {
            'session': [
                {'challengeName': 'SRP_A', 'challengeResult': False},
            ],
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'issueTokens': False,
            'failAuthentication': True,
        },
    }
