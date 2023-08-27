# cognito-email-mfa-using-custom-auth-challenges

This repository contains Cognito custom authentication challenge lamda triggers and an example script for Email MFA.

Please refer to the official documentation for Custom authentication challenge Lambda triggers.

https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-challenge.html

You may also refer to the blog post.

https://devnote.tech/2023/08/email-mfa-authentication-using-cognito-user-pool-custom-authentication-challenges/

## Requirements
- [Python 3](https://www.python.org/downloads/)
- [boto3](https://github.com/boto/boto3)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Amazon Simple Email Service for sending OTP codes

When you run the example script, you need to install the following:
- [warrant](https://github.com/capless/warrant/)
- [cryptography](https://github.com/pyca/cryptography/)
- [python-jose](https://github.com/mpdavis/python-jose/)

## Deploy
Run the following in your shell.

```shell
sam build
sam deploy --parameter-overrides EmailSender=<YOUR_SES_EMAIL_SENDER>
```

When completed, the following AWS resources are created in your AWS environment.

| Logical ID| Type |
| --------- | ---- |
| CognitoUserPool | AWS::Cognito::UserPool |
| CognitoUserPoolClient | AWS::Cognito::UserPoolClient |
| LambdaLayer | AWS::Lambda::LayerVersion |
| CreateAuthChallenge | AWS::Lambda::Function |
| DefineAuthChallenge | AWS::Lambda::Function |
| VerifyAuthChallenge | AWS::Lambda::Function |
| CreateAuthChallengeCognitoPermission | AWS::Lambda::Permission |
| DefineAuthChallengeCognitoPermission | AWS::Lambda::Permission |
| VerifyAuthChallengeCognitoPermission | AWS::Lambda::Permission |
| CreateAuthChallengeRole | AWS::IAM::Role |
| DefineAuthChallengeRole | AWS::IAM::Role |
| VerifyAuthChallengeRole | AWS::IAM::Role |

## Testing Email MFA
First of all, please create a Cognito user for testing by running the following command.

```shell
POOL_ID=<YOUR_USER_POOL_ID>
EMAIL=<YOUR_EMAIL>

# Add a Cognito user.
aws cognito-idp admin-create-user \
  --user-pool-id $POOL_ID \
  --username $EMAIL

# Make the user confirmation status "Confirmed"
echo -n 'Password: '
read password
aws cognito-idp admin-set-user-password \
  --user-pool-id $POOL_ID \
  --username $EMAIL \
  --password $password \
  --permanent
```

Run the example script using the following command.

```shell
cd src/example
pip install -r requirements.txt
python main.py \
  --pool-id <YOUR_USER_POOL_ID> \
  --client-id <YOUR_CLIENT_ID> \
  --username <YOUR_EMAIL> \
  --password <YOUR_PASSWORD>
```

## Cleanup
Run the following in your shell.

```shell
sam delete
```

## Unit Testing
Run the following in your shell.

```shell
export PYTHONPATH=$PYTHONPATH:$(pwd)/src:$(pwd)/src/layers/python
pytest -vv
```
