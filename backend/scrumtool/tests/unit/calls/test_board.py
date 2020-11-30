from django.test import TestCase
from rest_framework.test import APIRequestFactory
from scrumtool.api.models import Board

factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
