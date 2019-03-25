from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from datetime import datetime
import boto3
import logging
import json

from networkapi.wagtailpages.models import Petition

# Basket/Salesforce SQS client
crm_sqs = False

if settings.CRM_AWS_SQS_ACCESS_KEY_ID:
    crm_sqs = boto3.client(
        'sqs',
        region_name=settings.CRM_AWS_SQS_REGION,
        aws_access_key_id=settings.CRM_AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.CRM_AWS_SQS_SECRET_ACCESS_KEY,
    )


# sqs destination for salesforce
crm_queue_url = settings.CRM_PETITION_SQS_QUEUE_URL


logger = logging.getLogger(__name__)


@api_view(['POST'])
@parser_classes((JSONParser,))
@permission_classes((permissions.AllowAny,))
def petition_submission_view(request, pk):
    try:
        petition = Petition.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response(
            {'error': 'Invalid petition id'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return petition_submission(request, petition)


# handle Salesforce petition data
def petition_submission(request, petition):
    cid = petition.campaign_id

    if cid is None or cid == '':
        return Response(
            {'error': 'Server is missing campaign for petition'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    data = {
        "campaign_id": cid,
        "first_name": request.data['givenNames'],
        "last_name": request.data['surname'],
        "email": request.data['email'],
        "email_subscription": request.data['newsletterSignup'],
        "source_url": request.data['source'],
    }

    if petition.requires_country_code:
        if 'country' in request.data:
            data["country"] = request.data['country']
        else:
            return Response(
                {'error': 'Required field "country" is missing'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    if petition.requires_postal_code:
        if 'postalCode' in request.data:
            data["postal_code"] = request.data['postalCode']
        else:
            return Response(
                {'error': 'Required field "postalCode" is missing'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    policy = petition.comment_requirements
    if policy != 'none':
        if policy == 'optional' and 'comment' in request.data:
            data["comments"] = request.data['comment']
        elif policy == 'required':
            if 'comment' in request.data:
                data["comments"] = request.data['comment']
            else:
                return Response(
                    {'error': 'Required field "comment" is missing'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    message = json.dumps({
        'app': settings.HEROKU_APP_NAME,
        'timestamp': datetime.now().isoformat(),
        'data': {
            'json': True,
            'form': data,
            'event_type': 'crm_petition_data'
        }
    })

    return send_to_sqs(crm_sqs, crm_queue_url, message)


def send_to_sqs(sqs, queue_url, message):
    if settings.DEBUG is True:
        logger.info('Sending petition message: {}'.format(message))

        if not sqs:
            logger.info('Faking a success message (debug=true, sqs=nonexistent).')
            return Response({'message': 'success (faked)'}, 201)

    if queue_url is None:
        logger.warning('Petition was not submitted: No petition SQS url was specified')
        return Response({'message': 'success'}, 201)

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
    except Exception as error:
        logger.error('Failed to send petition with: {}'.format(error))
        return Response(
            {'error': 'Failed to queue up petition signup'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if 'MessageId' in response and response['MessageId']:
        return Response({'message': 'success'}, 201)
    else:
        return Response(
            {'error': 'Something went wrong with petition signup'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
