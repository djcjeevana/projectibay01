from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from Products.models import *


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        #response = self.c.get('')
        #self.assertEqual(response.status_code, 400)
        response = self.c.get('')
        self.assertEqual(response.status_code, 200)
        
        
    def test_product_detail_url(self):
           """
           Test items response status
           """
           response = self.c.get(
               reverse('Stores:product_single', args=['django-beginners']))
           self.assertEqual(response.status_code, 200)
