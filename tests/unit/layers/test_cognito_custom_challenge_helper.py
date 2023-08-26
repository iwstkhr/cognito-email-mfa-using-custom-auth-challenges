from layers.cognito_custom_challenge_helper import \
    CustomChallengeRequest, CustomChallengeResponse, Session, CustomChallengeName


class TestSession:
    def test_is_srp_a_1(self):
        session = {
            'challengeName': 'SRP_A',
            'challengeResult': True,
        }
        assert Session(session).is_srp_a() is True

    def test_is_srp_a_2(self):
        session = {
            'challengeName': 'SRP_A',
            'challengeResult': False,
        }
        assert Session(session).is_srp_a() is False

    def test_is_srp_a_3(self):
        session = {
            'challengeName': 'CUSTOM_CHALLENGE',
            'challengeResult': True,
        }
        assert Session(session).is_srp_a() is False

    def test_is_password_verifier_1(self):
        session = {
            'challengeName': 'PASSWORD_VERIFIER',
            'challengeResult': True,
        }
        assert Session(session).is_password_verifier() is True

    def test_is_password_verifier_2(self):
        session = {
            'challengeName': 'PASSWORD_VERIFIER',
            'challengeResult': False,
        }
        assert Session(session).is_password_verifier() is False

    def test_is_password_verifier_3(self):
        session = {
            'challengeName': 'CUSTOM_CHALLENGE',
            'challengeResult': True,
        }
        assert Session(session).is_password_verifier() is False

    def test_is_custom_challenge_1(self):
        session = {
            'challengeName': 'CUSTOM_CHALLENGE',
            'challengeResult': True,
        }
        assert Session(session).is_custom_challenge() is True

    def test_is_custom_challenge_2(self):
        session = {
            'challengeName': 'PASSWORD_VERIFIER',
            'challengeResult': True,
        }
        assert Session(session).is_custom_challenge() is False

    def test_can_issue_tokens_1(self):
        session = {
            'challengeName': 'CUSTOM_CHALLENGE',
            'challengeResult': True,
        }
        assert Session(session).can_issue_tokens() is True

    def test_can_issue_tokens_2(self):
        session = {
            'challengeName': 'CUSTOM_CHALLENGE',
            'challengeResult': False,
        }
        assert Session(session).can_issue_tokens() is False

    def test_can_issue_tokens_3(self):
        session = {
            'challengeName': 'PASSWORD_VERIFIER',
            'challengeResult': True,
        }
        assert Session(session).can_issue_tokens() is False


class TestCustomChallengeRequest:
    def test_verify_answer_1(self):
        event = {
            'request': {
                'challengeAnswer': '123456',
                'privateChallengeParameters': {'answer': '123456'},
                'userAttributes': {}
            },
            'response': {}
        }
        assert CustomChallengeRequest(event).verify_answer() is True

    def test_verify_answer_2(self):
        event = {
            'request': {
                'challengeAnswer': '12345',
                'privateChallengeParameters': {'answer': '123456'},
                'userAttributes': {}
            },
            'response': {}
        }
        assert CustomChallengeRequest(event).verify_answer() is False


class TestCustomChallengeResponse:
    def test_set_answer(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.set_answer('123456')
        assert response.__dict__()['privateChallengeParameters']['answer'] == '123456'

    def test_set_metadata(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.set_metadata('metadata')
        assert response.__dict__()['challengeMetadata'] == 'metadata'

    def test_set_next_challenge(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.set_next_challenge(CustomChallengeName.SRP_A)
        response_dict = response.__dict__()
        assert response_dict == {
            'challengeName': CustomChallengeName.SRP_A.value,
            'issueTokens': False,
            'failAuthentication': False,
        }

    def test_set_answer_correct(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.set_answer_correct(True)
        assert response.__dict__()['answerCorrect'] == True

    def test_issue_tokens(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.issue_tokens()
        response_dict = response.__dict__()
        assert response_dict == {
            'challengeName': '',
            'issueTokens': True,
            'failAuthentication': False,
        }

    def test_fail(self):
        event = {'response': {}}
        response = CustomChallengeResponse(event)
        response.fail()
        response_dict = response.__dict__()
        assert response_dict == {
            'issueTokens': False,
            'failAuthentication': True,
        }
