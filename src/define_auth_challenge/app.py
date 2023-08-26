# See https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html

from layers.cognito_custom_challenge_helper import CustomChallengeRequest, CustomChallengeResponse, CustomChallengeName


def lambda_handler(event: dict, context: dict) -> dict:
    # Parse the event to create a request and response object.
    request = CustomChallengeRequest(event)
    response = CustomChallengeResponse(event)
    last_session = request.last_session

    if last_session.is_srp_a():
        # When the last session is SRP_A, require the client to authenticate with a password.
        response.set_next_challenge(CustomChallengeName.PASSWORD_VERIFIER)

    elif last_session.is_password_verifier():
        # When the last session is PASSWORD_VERIFIER, initiate the custom challenge.
        response.set_next_challenge(CustomChallengeName.CUSTOM_CHALLENGE)

    elif last_session.is_custom_challenge():
        if last_session.can_issue_tokens():
            # When the last session is CUSTOM_CHALLENGE and authentication has been completed, issue tokens.
            response.issue_tokens()
        else:
            # When the last session is CUSTOM_CHALLENGE and the client is still during authentication flow,
            # require the client to answer the next challenge.
            response.set_next_challenge(CustomChallengeName.CUSTOM_CHALLENGE)
    else:
        # If the client is in an unexpected flow, the current authentication must fail.
        response.fail()

    event['response'] = response.__dict__()
    return event
