import json
import datetime
import time
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sqs = boto3.client('sqs')
dining_request_queue_url = 'https://sqs.us-east-1.amazonaws.com/869506624052/chatbotQueue'


# -- Lex Messages--

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


# ---Helper Functions------
def try_ex(func):
    try:
        return func()
    except KeyError:
        return None


def constructQueueMessage(location, cuisine, time, number, contact):
    number = str(number)
    contact = str(contact)
    message_attributes = {
        'Location': {
            'DataType': 'String',
            'StringValue': location
        },
        'DiningTime': {
            'DataType': 'String',
            'StringValue': time
        },
        'Cuisine': {
            'DataType': 'String',
            'StringValue': cuisine
        },
        'NumberOfPeople': {
            'DataType': 'String',
            'StringValue': number
        },
        'Contact': {
            'DataType': 'String',
            'StringValue': contact
        }

    }

    return message_attributes


# ---Fullfillment service---------
def send_msg_to_queue(message_attributes, contact):
    print('Sending to Queue {} to queue {}'.format(message_attributes, dining_request_queue_url))
    msg_body = 'Dining request for contact number {}'.format(str(contact))
    response = sqs.send_message(
        QueueUrl=dining_request_queue_url,
        DelaySeconds=10,
        MessageAttributes=message_attributes,
        MessageBody=msg_body
    )
    return response


def fullfill_dining_request(intent_request):
    '''
    code to full fill the dining request order
    '''
    print('In fullfill_dining_request......')
    slots = intent_request['currentIntent']['slots']

    location = try_ex(lambda: slots['Location'])
    cuisine = try_ex(lambda: slots['Cuisine'])
    time = try_ex(lambda: slots['Time'])
    number = try_ex(lambda: slots['Number'])
    contact = try_ex(lambda: slots['Contact'])

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    message_attributes = constructQueueMessage(location, cuisine, time, number, contact)
    response = send_msg_to_queue(message_attributes=message_attributes, contact=contact)

    if response['MessageId']:
        print('Fullfillment done')
        content = 'You’re all set. Expect my recommendations shortly!'
        return close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': content
            }
        )
    else:
        pass


def dispatch(intent_request):
    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'DiningSuggestionsIntent':
        return fullfill_dining_request(intent_request)
    else:
        raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
