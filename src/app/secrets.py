import json
import boto3
from botocore.exceptions import ClientError

def get_secret(key_name):

    secret_name = "prod/openai_linebot"
    # secret_name = "dev/openai_linebot"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret_values = get_secret_value_response['SecretString']
    return json.loads(secret_values)[key_name]
