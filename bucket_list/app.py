import json
import uuid

import boto3

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('bucket-list-items')
tableName = 'bucket-list-items'


def lambda_handler(event, context):
    # print(event)
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }
    print('Route Key: ' + event['routeKey'])
    try:
        if event['routeKey'] == "DELETE /bucket/list/{id}":
            table.delete_item(
                Key={'id': event['pathParameters']['id']})
            body = 'Deleted item ' + event['pathParameters']['id']
        elif event['routeKey'] == "GET /bucket/list/{id}":
            print("ID param ({}) ", event['pathParameters']['id'])
            body = table.get_item(
                Key={'id': event['pathParameters']['id']})
            print("Body : ({})", body)
            body = body["Item"]
            responseBody = [
                {'title': body['title'], 'description': body['description'], 'id': body['id']}]
            body = responseBody
        elif event['routeKey'] == "GET /bucket/list":
            body = table.scan()
            body = body["Items"]
            responseBody = []
            for items in body:
                responseItems = [
                    {'title': items['title'], 'description': items['description'], 'id': items['id']}]
                responseBody.append(responseItems)
            body = responseBody
        elif event['routeKey'] == "PUT /bucket/list":
            requestJSON = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'category': requestJSON['category'],
                    'title': requestJSON['title'],
                    'description': requestJSON['description']
                })
            body = requestJSON
    except KeyError as e:
        print("Error: " + str(e))
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
        print(body)
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    return res



