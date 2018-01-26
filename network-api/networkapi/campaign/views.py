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

from networkapi.campaign.models import Petition

if settings.AWS_SQS_ACCESS_KEY_ID:
    sqs = boto3.client(
        'sqs',
        use_ssl=False,
        region_name=settings.AWS_SQS_REGION,
        aws_access_key_id=settings.AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SQS_SECRET_ACCESS_KEY,
    )
queue_url = settings.PETITION_SQS_QUEUE_URL
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

    data = {
        'entry.1017670790': request.data['givenNames'],
        'entry.623318390': request.data['surname'],
        'entry.474888454': request.data['email'],
    }

    if petition.checkbox_1:
        data['entry.1822781637'] = 'Yes' if request.data['checkbox1'] is True else ''

    if petition.checkbox_2:
        data['entry.381347338'] = 'Yes' if request.data['checkbox2'] is True else ''

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

    if settings.DEBUG is True:
        logger.info('Sending petition message: {}'.format(message))

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
