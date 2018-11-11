import json
import boto3

lex_client = boto3.client('lex-runtime')


def lambda_handler(event, context):

    text = event["messages"]

    inputText = text.lower()


    response = lex_client.post_text(
        botName="chatbot",
        botAlias="chatbot",
        userId="dhaval",
        inputText=inputText
    )

    return response
