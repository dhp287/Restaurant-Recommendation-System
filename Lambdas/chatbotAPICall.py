import json
import boto3
from botocore.vendored import requests
from datetime import datetime, date
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/869506624052/chatbotQueue'
    sqs_client = boto3.client('sqs')
    resp = sqs_client.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['All'],
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=1
    )
    for k in range(len(resp)):
        msg = resp['Messages'][k]
        receipt_handle = msg['ReceiptHandle']

        attr = msg['MessageAttributes']
        loc = attr['Location']
        cuisine = attr['Cuisine']
        contact = attr['Contact']
        time = attr['DiningTime']
        no = attr['NumberOfPeople']

        ts = str(date.today().strftime("%m/%d/%Y")) + ' ' + time['StringValue'] + ':00'
        d = datetime.strptime(ts, '%m/%d/%Y %H:%M:%S')
        t = d.strftime("%s")
        url = 'https://api.yelp.com/v3/businesses/search?' + 'location=' + str(loc['StringValue']) + '&term=' + str(cuisine['StringValue']) + '&open_at=' + t + '&limit=' + str(3)
        headers = {"Authorization":"Bearer 2F6dTULd-mbARAOcjat5mbQCBpb9_dDVZ8yd_DdpgNfzfQtzzxL7IyQYQEXDfH6fqejFBM3TUgynbDvC7QT3X6zNB9Iu-rizfxjYFVlpSF14M_W3zQD_RxknX7nnW3Yx"}
        res = requests.get(url, headers=headers)

        sms = ''
        c = 1
        data = res.json()
        sms += 'We found ' + str(len(data['businesses'])) + ' restaurants for you:\n\n'
        for i in data['businesses']:
            sms += str(c) + '. Name: ' + str(i['name']) + '.\n'
            sms += 'Url: ' + str(i['url']) + '\n'
            sms += 'Rating: ' + str(i['rating']) + '\n'
            sms += 'Phone: ' + str(i['display_phone']) + '\n'
            sms += 'Address: '
            for j in i['location']['display_address']:
                sms += str(j) + ' '
            sms += '\n\n'
            c += 1

        dynamodb = boto3.resource('dynamodb')

        table = dynamodb.Table('chatbotTable')

        r = table.scan()
        id = len(r['Items']) + 1

        response = table.put_item(
        Item={
            'id': id,
            'contact': contact['StringValue'],
            'sms': sms

        }
        )

        client = boto3.client("sns", region_name="us-east-1")
        client.publish(PhoneNumber="+1"+str(contact['StringValue']), Message=sms)

        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

        print('Done')
