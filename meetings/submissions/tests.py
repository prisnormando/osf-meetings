from django.test import TestCase, RequestFactory
from unittest import skip
import factory
from submissions.models import Submission
from approvals.models import Approval
from conferences.models import Conference
from django.contrib.auth.models import User
from serializers import SubmissionSerializer
from views import SubmissionViewSet
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp

import ipdb


class UserFactory(factory.DjangoModelFactory):
    class Meta: 
        model = User

class ConferenceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Conference


class ApprovalFactory(factory.DjangoModelFactory):
    class Meta:
        model = Approval


class SubmissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Submission

    approval = factory.SubFactory(ApprovalFactory)

class SocialAccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialAccount

class SocialTokenFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialToken

class SocialAppFactory(factory.DjangoModelFactory):
    class Meta:
        model = SocialApp

class TestPermissions(TestCase):
    @skip('Test different permissions in many test functions')
    def test_permissions(self):
        pass


class TestSerializers(TestCase):

    def setUp(self):
        self.user = UserFactory(
            username = 'testUser'
            )
        self.request = RequestFactory().get('./fake_path')
        self.request.query_params = {}
        self.request.user = self.user
        self.submission = SubmissionFactory(
            contributor = self.user,
            conference = factory.SubFactory(ConferenceFactory, id='382', admin=factory.SubFactory(UserFactory, username='god'))
            )

    def test_get_links(self):
        serializer = SubmissionSerializer(context={'request': self.request})
        links = serializer.get_links(self.submission)
        self.assertEqual(links['self'], 'http://testserver/submissions/1/')
        self.assertEqual(links['conference'], 'http://testserver/conferences/382/')

    def test_get_can_edit(self):
        serializer = SubmissionSerializer(context={'request': self.request})
        submission2 = SubmissionFactory(
            contributor = factory.SubFactory(UserFactory, username='differentUser'),
            conference = factory.SubFactory(ConferenceFactory, id='234', admin=self.user)
            )
        submission3 = SubmissionFactory(
            contributor = factory.SubFactory(UserFactory, username='differentUser2'),
            conference = factory.SubFactory(ConferenceFactory, id = '18', admin=factory.SubFactory(UserFactory, username='differentUser3'))
            )
        self.assertTrue(serializer.get_can_edit(self.submission))
        self.assertTrue(serializer.get_can_edit(submission2))
        self.assertFalse(serializer.get_can_edit(submission3))


class TestSignals(TestCase):
    @skip('Test adding permissions via signal')
    def test_add_permissions_approved(self):
        pass

    @skip('Test adding permissions via signal')
    def test_add_permissions_rejected(self):
        pass


class TestViews(TestCase):

    def setUp(self):
        self.user = UserFactory(
            username='testViewsUser',
            id='428'
            )
        self.socialAccount = SocialAccountFactory(
            user=self.user,
            uid='testViewsUser'
            )
        self.socialToken = SocialTokenFactory(
            account = self.socialAccount,
            app = factory.SubFactory(SocialAppFactory)
            )
        self.approval = ApprovalFactory(
            id=1,
            approved=True
        )
        self.conference = ConferenceFactory(
            admin = self.user,
            id = 'conferenceId'
            )
        self.request = RequestFactory().post('./fake_path')
        self.request.user = self.user
        self.request.query_params = {}
        self.contributorData = {'type': 'User', 'username': 'testViewsUser', 'id': '428'}
        self.approvalData = {'type': 'Approval', 'approved': True, 'id': 1}
        self.conferenceData = {'type': 'conferences', 'id': 'conferenceId'}
        self.request.data = {'id': 15, 'node_id': '42u2p', 'title': 'Submission65', 'contributor': self.contributorData, 
                'description': 'This is a submission', 'approval': self.approvalData, 'conference': self.conferenceData}
        self.views = SubmissionViewSet()

    def test_create(self):
        self.views.create(self.request)
        ipdb.set_trace()

    @skip('Test queryset')
    def test_get_queryset(self):
        pass

    @skip('Relationship view, is this duplicating?')
    def test_relationship(self):
        pass
