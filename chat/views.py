from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.db.models import Avg
from django.db.models import Func, F

from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.core.cache import cache

from rest_framework.response import Response

from django.db.models import Avg
from django.db.models import Func, F

from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.core.cache import cache

import datetime
import time
import os


def index(request):
    # return render(request, 'chat/index.html', {})
    return Response(1, status=status.HTTP_200_OK)


def room(request):
    return Response(1, status=status.HTTP_200_OK)

    # return render(request, 'chat/room.html', {
    #     'room_name_json': mark_safe(json.dumps(room_name))
    # })


class RoomView(APIView):
    def get(self, request):
        now = datetime.datetime.now().replace(
            minute=0, second=0, microsecond=0)
        # cache_key = self.c_key(now, l_num=0)
        # response_ = cache.get(cache_key, None)
        # if not response_:
        #     response_ = self.result(now, l_num=0)
        #     cache.set(cache_key, response_, 60*60)

        # print(pd.DataFrame(response_['prediction'], columns=response_.keys()))
        return Response(now, status=status.HTTP_200_OK)

