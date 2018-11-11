import json
import datetime
import time
import os
import dateutil.parser
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# --Helper Functions to build response

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):

    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


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



# --Helper Functions
def try_ex(func):
    try:
        return func()
    except KeyError:
        return None


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_text(text):
    if not text or not text.isalpha():
        return False
    else:
        return True

def isvalid_city(city):
    valid_cities = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
                    'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
                    'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc',
                    'memphis', 'boston', 'nashville', 'baltimore', 'portland']
    return city.lower() in valid_cities

def isvalid_cuisine(cuisine):
    cuisine_types = ['thai', 'american', 'mexican', 'chinese', 'indian', 'japanese', 'italian']
    return cuisine.lower() in cuisine_types


def validateDinningSuggestionsIntent(slots):
    location = try_ex(lambda: slots['Location'])
    cuisine = try_ex(lambda: slots['Cuisine'])
    time = try_ex(lambda: slots['Time'])
    number = try_ex(lambda: slots['Number'])

    if not location:
        return build_validation_result(
            False,
            'Location',
            'Enter a location?'
        )

    if not isvalid_city(location):
        return build_validation_result(
            False,
            'Location',
            'We don\'t know about {} city, try other option'.format(location)
        )

    if not cuisine:
        return build_validation_result(
            False,
            'Cuisine',
            'What cuisine?'
        )

    if not isvalid_cuisine(cuisine):
        return build_validation_result(
            False,
            'Cuisine',
            'We don\'t know about {} cuisine, try other option'.format(cuisine)
        )
    return {'isValid': True}


# ---Intents---

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug(
        'dispatch userID: {},intentName:{} '.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    logger.debug('Session Attribute {}'.format(session_attributes))
    print(intent_request)
    # Dispatch to intents
    if intent_request['invocationSource'] == 'DialogCodeHook':

        if (intent_name == 'DiningSuggestionsIntent'):
            logger.debug('Validating slots for DiningSuggestionsIntent....')
            validation_result = validateDinningSuggestionsIntent(intent_request['currentIntent']['slots'])


        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        else:
            return delegate(
                session_attributes,
                intent_request['currentIntent']['slots']
                )
    else:
        pass

# Main Halder for validations
def lambda_handler(event, context):
    """
    Route incoming request based on intent

    """
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    print(event)
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)

    
