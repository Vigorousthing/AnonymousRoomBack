from rest_framework.response import Response

from django.db.models import Avg
from django.db.models import Func, F

from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.core.cache import cache

import pandas as pd
import datetime
import time
import os

