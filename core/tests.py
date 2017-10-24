# -*- coding: utf-8 -*-

import json
import mock

from django.http import JsonResponse
from django.test import TestCase

from core.utils import is_title, split_sentences
from core.views import sentence_split


class SentenceSplitTest(TestCase):

    def test_split(self):
        txt = u'''
This Agreement covers the provisions of broadband access, Internet, voice, data, Managed Broadband Services, Hosting Services, Applications and Voice-Over-IP and all others services ("Services") from Blackfoot pursuant to orderslaced by Customer and accepted by Blackfoot, as defined below and described in one or more Service Order Forms executed by Customer and Blackfoot (“Service Orders”). This Agreement includes each such Service Order, including any attachments or exhibits thereto, and all of the attachments to this Agreement. Please note that underlined terms in this Agreement are links to pages and websites where such attachments, each of which is incorporated herein by reference, may be reviewed by Customer.

CUSTOMER MUST READ, AGREE WITH AND ACCEPT ALL OF THE TERMS AND CONDITIONS OF THIS AGREEMENT, INCLUDING THE SERVICE ORDERS AND ATTACHMENTS INCORPORATED HEREIN BY REFERENCE, BEFORE USING OR ACCEPTING ANY BLACKFOOT SERVICES. IF CUSTOMER DOES NOT AGREE TO BE BOUND BY THE TERMS AND CONDITIONS OF THIS AGREEMENT, CUSTOMER MAY NOT, AND SHALL HAVE NO RIGHT TO, USE ANY BLACKFOOT SERVICES.



By accepting this Agreement, Customer agrees that its use of our Services will be governed by, and in accordance with, the terms and conditions hereof. Blackfoot may amend this Agreement at any time by posting the amended terms on its web site. All amended terms shall become effective upon Blackfoot posting such amended Agreement on its web site.
'''
        sentences = split_sentences(txt)
        self.assertEqual(len(sentences), 8)
        self.assertEqual(''.join(sentences), txt)

    def test_split_additional(self):
        txt = u'''
These Terms of Service (as defined below) are legally binding and govern all Your (as defined below) use of all Services (as defined below) offered by Buildscale Inc., operating as Vidyard, (“Buildscale”, “Our”, “Us” or “We”).

PLEASE READ THESE TERMS OF SERVICE CAREFULLY. THESE TERMS OF SERVICE SETS FORTH THE LEGALLY BINDING TERMS AND CONDITIONS FOR YOUR USE OF THE VIDYARD SERVICES AND INCLUDES GRANTS OF RIGHTS TO US AND LIMITATIONS ON OUR LIABILITY. YOU SHOULD PRINT A COPY OF THESE TERMS OR SAVE THEM ON YOUR DEVICE IN THE EVENT THAT YOU NEED TO REFER TO THEM IN THE FUTURE.
1. INTRODUCTION

1.1 Scope. The services offered by Buildscale include (collectively, “Services”): (i) those offered on any Vidyard-branded URL, including  www.vidyard.com (the “Website”);(ii) Vidyard (as defined below); (iii) the Player; (iv) Buildscale or Vidyard developer services; (v) Buildscale or Vidyard apps; (vi) technical support; (vii) Professional Services; and (vi) any other features, content, or applications offered or operated from time to time by Buildscale in connection with Buildscale’s business, including when Vidyard is accessed via the internet, mobile device, television or other device. These Terms of Service constitutes legally binding terms and applies to such use of the Services regardless of the type of device used to access them ("Device") unless such services post a different terms of use or end user license agreement, in which case that agreement ("Other Terms") shall instead govern. By accessing and/or using any of the Services, You agree to be bound by these Terms of Service (or if applicable, the Other Terms), whether You are a "Visitor" (which means that You simply browse the Services, including, without limitation, through a mobile or other wireless Device, or otherwise use the Services and/or access and view Content (as defined below) without being registered) or You are a "Customer" (which means that You have registered with Buildscale). The term "User" refers to a Visitor or a Customer. You are authorized to use the Services (regardless of whether Your access or use is intended) only if You agree to abide by all applicable laws, rules and regulations ("Applicable Law") and the terms of these Terms of Service. In addition, in consideration for becoming a Customer and/or making use of the Services, You must indicate Your acceptance of these Terms of Service during the registration process. Thereafter, You may create Your Account (as defined below), and its associated profile(s) in accordance with the terms herein.
'''
        sentences = split_sentences(txt)
        self.assertEqual(len(sentences), 13)
        self.assertEqual(''.join(sentences), txt)

    def test_split_quote(self):
        txt = u'It\'s "confidential." More text.'
        sentences = split_sentences(txt)
        self.assertEqual(len([s for s in sentences if s]), 2)

    def test_split_unicode(self):
        """ Check that it doesn't blow up when fed unicode """
        split_sentences(u'All information regarding either Party’s business which has been marked or is otherwise communicated as being “proprietary” or “confidential.”')

    # --- Specific test cases ---

    def test_not_splitting_on_inc(self):
        texts = [
            'Beagle Inc. will do that.',
            'Blackfoot Communications, Inc.("Blackfoot"), provides services to its customers ("Customer").'
        ]

        for txt in texts:
            sentences = split_sentences(txt)
            self.assertEqual(len([s for s in sentences if s]), 1)

    def test_not_splitting_on_bullets(self):
        """ Some '. 's should not be sentence splitters """
        texts = [
            '- Beagle will do that.',
            '10. Beagle will do that.',
            'i. Blackleg Communications provides services to its customers ("Customer").',
            'iii. Communications provides services',
            'a. Communications provides services',
            'D. Communications provides services.',
            'et. al. etc. these are valid',
        ]

        for txt in texts:
            sentences = split_sentences(txt)
            self.assertEqual(len([s for s in sentences if s]), 1)

    def test_not_splitting_on_acronyms(self):
        """ Some '. 's should not be sentence splitters """
        texts = [
            'Inc. brand.',
            'Beagle Inc. will do that.',
            'BEAGLE INC. DOES EVERYTHING.',
            'Beagle Inc. COMMUNICATIONS PROVIDES SERVICES',
            u'This Master Subscription Agreement (the "Agreement") is entered into as of ____________, 2015 (“Effective Date”) by and between Axonify Inc., a Canadian Corporation having its registered office at 460 Phillip St. Suite 300, Waterloo, ON N2L 5J2 ("Axonify Inc.") and Shinydocs Corporation having its principal place of business at 108 Ahrens St W #8b, Kitchener, ON N2H 4C3 ("Customer").',
            u'This Master Services Agreement (the “Agreement” or "MSA") describes the terms on which Blackfoot Communications, Inc. (“Blackfoot”), provides services to its customers ("Customer").',
        ]

        for txt in texts:
            sentences = split_sentences(txt)
            self.assertEqual(len([s for s in sentences if s]), 1)

    def test_not_merging_wanted_splits(self):
        """ Assert the merger is not too permisive """
        texts = [
            'Ahoy. Howdy?',
            '$60. Damn bike rental!',
            'mahjong. Communications provides services',
        ]

        for txt in texts:
            sentences = split_sentences(txt)
            self.assertEqual(len([s for s in sentences if s]), 2)

    def test_bullets_merge(self):
        txt = u'''Non-Solicitation.\t
20. Any attempt.'''
        sentences = split_sentences(txt)
        self.assertEqual(sentences, [u'Non-Solicitation.\t\n', u'20. Any attempt.'])

    def test_bslashr(self):
        txt = u'''Non-Solicitation.\r20. Any attempt.'''
        sentences = split_sentences(txt)
        self.assertEqual(sentences, [u'Non-Solicitation.\r', u'20. Any attempt.'])

    def test_split_title(self):
        txt = u'''
            Terms of Agreement
            This Terms of Agreement, including its Addenda and Schedules governs terms and conditions between X, Y and Z.
            1. Definitions
            1.1. Acceptable Use Policy means the applicable terms and conditions governing the use by End Users of a specific Product, Service or Application, as may be identified on the Fees and Rates Schedule.
            1.2. Active User means a License Model that accounts for any person who registers for or is enrolled in one or more courses in each consecutive 12-month period following the Effective Date.
            This sentence was intentionally split into two lines,
            and it doesn't contain any title.
        '''
        sentences = split_sentences(txt)
        self.assertEqual(len(sentences), 6)
        self.assertEqual(''.join(sentences), txt)

    def check_is_title(self, clause, expected):
        actual = is_title(clause)
        self.assertEqual(expected, actual)

    def test_is_title(self):
        self.check_is_title(' \t \n \t ', False)
        self.check_is_title('', False)

        self.check_is_title('London is the capital of Great Britain', False)

        self.check_is_title('Python for Biologists', True)
        self.check_is_title('Learn Python the Hard Way', True)
        self.check_is_title('Hacking Secret Ciphers with Python', True)
        self.check_is_title('Automate the Boring Stuff with Python', True)

        for clause in ['Definitions',
                       'Billing and Payment Terms',
                       'Description of Services, Rates and Charges',
                       'Use of the Service Offerings',
                       'Security and Data Privacy',
                       'Owner\'s Representative; Inspection of Work',
                       'Dispute Resolution and Governing Law',
                       'Disclaimers and Limitations of Liability',
                       'Compliance with Applicable Laws',
                       'Ownership and Intellectual Property Rights',
                       'Account Termination Policy',
                       'Copyright Notice']:

            for bullet in ['1', 'iv', 'G', 'c', '7', 'XI', 'v', '9', 'N']:
                self.check_is_title('\t%s. %s\n' % (bullet, clause), True)
                self.check_is_title('\t%s. %s:\n' % (bullet, clause), False)
                self.check_is_title('\t%s. \n' % bullet, False)

            self.check_is_title(clause, True)
            self.check_is_title(clause.lower(), False)
            self.check_is_title(clause.upper(), len(clause.split()) <= 4)


class APITest(TestCase):

    @staticmethod
    def mock_request(method=None, content_type=None, META=None, body=None):
        request = mock.MagicMock()
        request.method = method or 'POST'
        request.content_type = content_type or 'application/json'
        request.META = META or {'HTTP_X_ACCESS_TOKEN': 'qwerty'}
        request.body = body or '{"text": "Hello, world!  My name is Gevorg. I am fond of sentence splitting."}'
        return request

    def assert_failure(self, response, expected_data, expected_status_code):
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(expected_data, json.loads(response.content))
        self.assertEqual(expected_status_code, response.status_code)

    def assert_success(self, response, expected_data):
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(expected_data, json.loads(response.content))
        self.assertEqual(200, response.status_code)

    def test_not_post(self):
        for method in ['GET', 'DELETE', 'PUT']:
            request = self.mock_request(method=method)
            response = sentence_split(request)
            self.assert_failure(response, {"error": "POST method expected"}, 400)

    def test_not_json(self):
        for content_type in ['text/plain', 'application/javascript', 'application/xml', 'text/xml', 'text/html']:
            request = self.mock_request(content_type=content_type)
            response = sentence_split(request)
            self.assert_failure(response, {"error": "application/json content type expected"}, 400)

    def test_no_token(self):
        request = self.mock_request(META={'foo': 'bar'})
        response = sentence_split(request)
        self.assert_failure(response, {"error": "x-access-token header expected"}, 400)

    @mock.patch('core.models.AccessToken.objects.filter', return_value=False)
    def test_invalid_token(self, access_token_filter_mock):
        request = self.mock_request()
        response = sentence_split(request)
        access_token_filter_mock.assert_called_once_with(value='qwerty')
        self.assert_failure(response, {"error": "access denied (invalid token)"}, 403)

    @mock.patch('core.models.AccessToken.objects.filter', return_value=True)
    def test_invalid_body(self, access_token_filter_mock):
        request = self.mock_request(body='Some invalid JSON string')
        response = sentence_split(request)
        access_token_filter_mock.assert_called_once_with(value='qwerty')
        self.assert_failure(response, {"error": "JSON body expected"}, 400)

    @mock.patch('core.models.AccessToken.objects.filter', return_value=True)
    def test_no_text(self, access_token_filter_mock):
        request = self.mock_request(body='{"foo": "bar"}')
        response = sentence_split(request)
        access_token_filter_mock.assert_called_once_with(value='qwerty')
        self.assert_failure(response, {"error": "'text' key in body expected"}, 400)

    @mock.patch('core.models.AccessToken.objects.filter', return_value=True)
    def test_ok(self, access_token_filter_mock):
        request = self.mock_request()
        response = sentence_split(request)
        access_token_filter_mock.assert_called_once_with(value='qwerty')
        self.assert_success(response, ["Hello, world!  ", "My name is Gevorg. ", "I am fond of sentence splitting."])
