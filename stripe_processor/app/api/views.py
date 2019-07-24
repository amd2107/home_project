# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import ProcessCardSerializer
from app.api.process_card import ProcessCard

class ProcessCardAPIView(CreateAPIView):

    serializer_class = ProcessCardSerializer
    process_card = ProcessCard()

    def post(self, request, *args, **kwargs):

        data = request.data

        process_card_serializer = ProcessCardSerializer(data = data)

        if not process_card_serializer.is_valid():
            content = {
            'success': False,
            'message': process_card_serializer.errors
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        response = self.process_card.process(data)

        if not response['success']:
            content = {
            'success': False,
            'message': response['error']
            }

            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'success': True,
                'data':response['data']
                
            },
            status=status.HTTP_201_CREATED
        )

