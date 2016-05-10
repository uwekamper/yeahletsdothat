# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from __future__ import unicode_literals
import json
import pytest

@pytest.mark.django_db
def test_campaign_creation():
    """
    Test if we can create an activity.
    """
    pass
    #campaign = mommy.make(Campaign)
    #assert isinstance(campaign, Campaign)


# class BankAccountTest(TestCase):
#
#     TEST_DESCRIPTION = 'testaccount'
#
#     def setUp(self):
#         self.acc = mommy.make(BankAccount, description=self.TEST_DESCRIPTION)
#
#     def test_can_create_account(self):
#         self.assertIsInstance(self.acc, BankAccount)
#
#     def test_get_unicode(self):
#         self.assertEqual(str(self.acc), self.TEST_DESCRIPTION)





