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

# Google sheet SQS client
gs_sqs = False

if settings.AWS_SQS_ACCESS_KEY_ID:
    gs_sqs = boto3.client(
        'sqs',
        region_name=settings.AWS_SQS_REGION,
        aws_access_key_id=settings.AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SQS_SECRET_ACCESS_KEY,
    )

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

# sqs destination for google sheets
gs_queue_url = settings.PETITION_SQS_QUEUE_URL

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

    if petition.legacy_petition is True:
        return legacy_petition_submission(request, petition)
    else:
        return petition_submission(request, petition)


# handle Google-sheet petition data
def legacy_petition_submission(request, petition):
    data = {
        petition.given_name_form_field: request.data['givenNames'],
        petition.surname_form_field: request.data['surname'],
        petition.email_form_field: request.data['email'],
        petition.newsletter_signup_form_field: 'Yes' if request.data['newsletterSignup'] is True else 'No'
    }

    if petition.checkbox_1:
        data[petition.checkbox_1_form_field] = 'Yes' if request.data['checkbox1'] is True else 'No'

    if petition.checkbox_2:
        data[petition.checkbox_2_form_field] = 'Yes' if request.data['checkbox2'] is True else 'No'

    message = json.dumps({
        'app': settings.HEROKU_APP_NAME,
        'event_type': 'send_post_request',
        'timestamp': datetime.now().isoformat(),
        'data': {
            'url': petition.google_forms_url,
            'json': True,
            'form': data
        }
    })

    return send_to_sqs(gs_sqs, gs_queue_url, message)


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
        # We already submit an email subscription separately
        # on the client side, so we should check whether
        # this will cause something to receive a sign-up
        # thank you email twice, or only once:
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
