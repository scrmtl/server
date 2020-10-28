'''from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.models import Board

factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
'''
import os

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient


from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from api.models import Board

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class TestBoardUrl(SimpleTestCase):
    def setUp(self):
        client_id = '3XUwGn9Dzf7VyLdICjELa47xt0esHTVkrIxMDnVR'
        client_secret = 'g7u7l6ic6xCV84bLjOPno5YqrElztwrFchPOLQi4bavzKMN0mURl\
            MsZT70FpRcbNTpJGuenYlPKKLPN56w3RSWzCpaW4TcpACbucpLPDvoPsXqWzblE\
                MNQwBFSl77eUy'
        self.token_url = 'http://192.168.178.48:14444/o/token/'
        '''
        client = BackendApplicationClient(
            client_id,
            scope='read')
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url=token_url,
                                       client_id=client_id,
                                       client_secret=client_secret)
                                       '''

    def test_board_(self):
        factory = APIRequestFactory()
        request = factory.get('/boards/')
        # force_authenticate(request, user=user)
        # print(request.)
