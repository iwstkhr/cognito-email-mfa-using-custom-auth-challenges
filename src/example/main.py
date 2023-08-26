""" Email MFA authentication using Cognito user pool custom authentication challenges

This script is an example of Email MFA.
"""

import argparse
from argparse import Namespace

import boto3
from warrant import AWSSRP

session = boto3.Session()
client = session.client('cognito-idp')


def get_aws_srp(args: Namespace) -> AWSSRP:
    return AWSSRP(
        username=args.username,
        password=args.password,
        pool_id=args.pool_id,
        client_id=args.client_id,
    )


def initiate_auth(awssrp: AWSSRP):
    # Authenticate to Cognito User Pool
    awssrp.authenticate_user()

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/initiate_auth.html
    # For CUSTOM_AUTH: USERNAME (required), SECRET_HASH (if app client is configured with client secret), DEVICE_KEY.
    # To start the authentication flow with password verification, include ChallengeName: SRP_A and SRP_A: (The SRP_A Value).
    return client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={
            'USERNAME': awssrp.username,
            'CHALLENGE_NAME': 'SRP_A',
            'SRP_A': hex(awssrp.large_a_value)[2:],
        },
        ClientId=awssrp.client_id,
    )


def respond_to_auth_challenge(awssrp: AWSSRP, prev_response: dict):
    challenge_responses = awssrp.process_challenge(prev_response['ChallengeParameters'])

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/respond_to_auth_challenge.html
    return client.respond_to_auth_challenge(
        ClientId=awssrp.client_id,
        ChallengeName=prev_response['ChallengeName'],
        Session=prev_response['Session'],
        ChallengeResponses=challenge_responses,
    )


def respond_to_custom_challenge(awssrp: AWSSRP, prev_response: dict):
    # Require OTP code sent from the Cognito custom challenge Lamda.
    code = input(f'Code: ')

    return client.respond_to_auth_challenge(
        ClientId=awssrp.client_id,
        ChallengeName=prev_response['ChallengeName'],
        Session=prev_response['Session'],
        ChallengeResponses={'USERNAME': awssrp.username, 'ANSWER': code},
    )


def parse_args() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--pool-id', type=str, required=True)
    parser.add_argument('--client-id', type=str, required=True)
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    awssrp = get_aws_srp(args)

    response = initiate_auth(awssrp)
    response = respond_to_auth_challenge(awssrp, response)

    while True:
        response = respond_to_custom_challenge(awssrp, response)
        if response.get('ChallengeName') == 'CUSTOM_CHALLENGE':
            # OTP is incorrect.
            print('Authentication failed.')
            continue

        # OTP is correct.
        print('Authentication succeeded.')
        break


if __name__ == '__main__':
    main()
