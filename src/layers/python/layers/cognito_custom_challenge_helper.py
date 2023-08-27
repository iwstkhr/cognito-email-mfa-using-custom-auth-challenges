import copy
from enum import Enum


class CustomChallengeName(Enum):
    SRP_A = 'SRP_A'
    PASSWORD_VERIFIER = 'PASSWORD_VERIFIER'
    CUSTOM_CHALLENGE = 'CUSTOM_CHALLENGE'


class Session:
    def __init__(self, session: dict):
        _session = copy.deepcopy(session)
        self.challenge_name = _session['challengeName']
        self.challenge_result = _session['challengeResult']
        self.challenge_metadata = _session.get('challengeMetadata', '')

    def is_srp_a(self) -> bool:
        return self.challenge_name == CustomChallengeName.SRP_A.value \
            and self.challenge_result is True

    def is_password_verifier(self) -> bool:
        return self.challenge_name == CustomChallengeName.PASSWORD_VERIFIER.value \
            and self.challenge_result is True

    def is_custom_challenge(self) -> bool:
        return self.challenge_name == CustomChallengeName.CUSTOM_CHALLENGE.value

    def can_issue_tokens(self) -> bool:
        return self.is_custom_challenge() and self.challenge_result is True


class CustomChallengeRequest:
    def __init__(self, event: dict):
        _request = copy.deepcopy(event['request'])
        _session = _request.get('session', [])
        self.last_session = Session(_session[-1]) if _session else None
        self.user_attributes = _request['userAttributes']
        self.challenge_answer = _request.get('challengeAnswer', '')
        self.private_challenge_parameters = _request.get('privateChallengeParameters', {})

    def verify_answer(self) -> bool:
        return self.private_challenge_parameters.get('answer') == self.challenge_answer


class CustomChallengeResponse:
    def __init__(self, event: dict):
        _response = copy.deepcopy(event['response'])
        self._response = _response

    def set_answer(self, answer: str) -> None:
        self._response['privateChallengeParameters'] = {}
        self._response['privateChallengeParameters']['answer'] = answer

    def set_metadata(self, data: str) -> None:
        self._response['challengeMetadata'] = data

    def set_next_challenge(self, name: CustomChallengeName) -> None:
        self._response['challengeName'] = name.value
        self._response['issueTokens'] = False
        self._response['failAuthentication'] = False

    def set_answer_correct(self, correct: bool) -> None:
        self._response['answerCorrect'] = correct

    def issue_tokens(self) -> None:
        self._response['challengeName'] = ''
        self._response['issueTokens'] = True
        self._response['failAuthentication'] = False

    def fail(self) -> None:
        self._response['issueTokens'] = False
        self._response['failAuthentication'] = True

    def __dict__(self) -> dict:
        return self._response
