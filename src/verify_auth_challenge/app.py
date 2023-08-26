# See https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html

from layers.cognito_custom_challenge_helper import CustomChallengeRequest, CustomChallengeResponse


def lambda_handler(event: dict, context: dict) -> dict:
    # Parse the event to create a request and response object.
    request = CustomChallengeRequest(event)
    response = CustomChallengeResponse(event)

    # Create a response.
    correct = request.verify_answer()
    response.set_answer_correct(correct)
    event['response'] = response.__dict__()
    return event
