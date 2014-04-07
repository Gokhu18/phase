import datetime

from django.test import TestCase

from categories.factories import CategoryFactory
from documents.factories import DocumentFactory
from accounts.factories import UserFactory


class ReviewMixinTests(TestCase):

    def setUp(self):
        self.category = CategoryFactory()
        self.user = UserFactory(
            email='testadmin@phase.fr',
            password='pass',
            is_superuser=True,
            category=self.category
        )

    def create_reviewable_document(self):
        doc = DocumentFactory(
            category=self.category,
            revision={
                'leader': self.user,
                'approver': self.user,
                'reviewers': [self.user],
            }
        )
        return doc.latest_revision

    def test_new_doc_cannot_be_reviewed(self):
        doc = DocumentFactory(category=self.category)
        self.assertFalse(doc.latest_revision.can_be_reviewed())

    def test_doc_without_reviewers_cannot_be_reviewed(self):
        doc = DocumentFactory(category=self.category)
        revision = doc.latest_revision
        revision.leader = self.user
        revision.approver = self.user
        revision.save()

        self.assertFalse(revision.can_be_reviewed())

    def test_doc_can_be_reviewed(self):
        revision = self.create_reviewable_document()
        self.assertTrue(revision.can_be_reviewed())

    def test_doc_can_only_be_reviewed_once(self):
        revision = self.create_reviewable_document()
        revision.review_start_date = datetime.date.today()
        revision.save()

        self.assertFalse(revision.can_be_reviewed())

    def test_start_review_process(self):
        revision = self.create_reviewable_document()
        self.assertIsNone(revision.review_start_date)
        self.assertIsNone(revision.review_due_date)
        self.assertIsNone(revision.review_end_date)
        self.assertIsNone(revision.reviewers_step_closed)
        self.assertIsNone(revision.leader_step_closed)

        revision.start_review()
        today = datetime.date.today()
        in_two_weeks = today + datetime.timedelta(days=14)

        self.assertEqual(revision.review_start_date, today)
        self.assertEqual(revision.review_due_date, in_two_weeks)

    def test_end_reviewers_step(self):
        revision = self.create_reviewable_document()
        revision.start_review()

        revision.end_reviewers_step()
        today = datetime.date.today()
        self.assertEqual(revision.reviewers_step_closed, today)

    def test_end_leader_step(self):
        revision = self.create_reviewable_document()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        revision.review_start_date = yesterday
        revision.reviewers_step_closed = yesterday

        revision.end_leader_step()

        self.assertEqual(revision.reviewers_step_closed, yesterday)
        self.assertEqual(revision.leader_step_closed, today)

    def test_end_leader_step_with_reviewers_step_open(self):
        revision = self.create_reviewable_document()
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        revision.review_start_date = yesterday

        revision.end_leader_step()

        self.assertEqual(revision.reviewers_step_closed, today)
        self.assertEqual(revision.leader_step_closed, today)

    def test_end_review_process(self):
        revision = self.create_reviewable_document()

        revision.start_review()
        revision.end_review()

        today = datetime.date.today()
        self.assertEqual(revision.reviewers_step_closed, today)
        self.assertEqual(revision.leader_step_closed, today)
        self.assertEqual(revision.review_end_date, today)

    def test_is_under_review(self):
        doc = DocumentFactory(category=self.category)
        revision = doc.latest_revision
        revision.leader = self.user
        revision.approver = self.user
        revision.reviewers.add(self.user)
        revision.save()

        self.assertFalse(revision.is_under_review())

        revision.start_review()
        self.assertTrue(revision.is_under_review())

        revision.end_review()
        self.assertFalse(revision.is_under_review())

    def test_is_overdue(self):
        doc = DocumentFactory(category=self.category)
        revision = doc.latest_revision
        revision.leader = self.user
        revision.approver = self.user
        revision.reviewers.add(self.user)
        revision.save()

        self.assertFalse(revision.is_overdue())

        today = datetime.date.today()
        revision.review_due_date = today + datetime.timedelta(days=1)
        self.assertFalse(revision.is_overdue())

        revision.review_due_date = today - datetime.timedelta(days=1)
        self.assertTrue(revision.is_overdue())

        revision.review_due_date = today
        self.assertFalse(revision.is_overdue())

    def test_current_step(self):
        revision = self.create_reviewable_document()

        self.assertEqual(revision.current_step(), 'new')

        revision.start_review()
        self.assertEqual(revision.current_step(), 'reviewers')

        revision.end_reviewers_step()
        self.assertEqual(revision.current_step(), 'leader')

        revision.end_leader_step()
        self.assertEqual(revision.current_step(), 'approver')

        revision.end_review()
        self.assertEqual(revision.current_step(), 'closed')
