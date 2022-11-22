from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    @action(detail=True, methods=['get'])
    def info_one_mailing(self, request, pk=None):
        """"Detailed statistics of messages on a specific mailing"""

        mailing = Mailing.objects.all()
        get_object_or_404(mailing, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def info_all_mailings(self, request):
        ml_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        result = {}

        for row in mailing:
            res = {
                'Count of messages': 0,
                'Sent messages': 0,
                'No sent messages': 0
            }
            mail = Message.objects.filter(mailing_id=row['id']).all()
            msg_sent = mail.filter(sending_status='Sent').count()
            msg_no_sent = mail.filter(sending_status='No sent').count()
            res['Total messages'] = len(mail)
            res['Sent'] = msg_sent
            res['No sent'] = msg_no_sent
            result[row['id']] = res

        content = {'Total number of mailings': ml_count,
                   'The number of messages sent': result}
        return Response(content)
