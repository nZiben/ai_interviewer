"""Amazon Polly Integration"""
import boto3
from botocore.exceptions import BotoCoreError, ClientError

class AmazonPollyTTS:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str = 'us-east-1'):
        self.polly = boto3.client(
            'polly',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def text_to_speech(self, text: str) -> bytes:
        try:
            response = self.polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId='Joanna'
            )
            return response['AudioStream'].read()
        except (BotoCoreError, ClientError) as e:
            return b""
