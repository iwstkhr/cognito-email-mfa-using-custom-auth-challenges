from verify_auth_challenge import app


def test_lambda_handler_1():
    """ When answer correct """

    event = {
        'request': {
            'challengeAnswer': '123456',
            'privateChallengeParameters': {'answer': '123456'},
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'answerCorrect': True
        }
    }


def test_lambda_handler_2():
    """ When answer incorrect """

    event = {
        'request': {
            'challengeAnswer': '12345',
            'privateChallengeParameters': {'answer': '123456'},
            'userAttributes': {}
        },
        'response': {}
    }
    result = app.lambda_handler(event, {})
    assert result == {
        'request': event['request'],
        'response': {
            'answerCorrect': False
        }
    }
