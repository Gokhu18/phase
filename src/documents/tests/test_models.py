from django.test import TestCase

from documents.models import Document, DocumentRevision


class DocumentTest(TestCase):

    def test_document_number(self):
        """
        Tests that a document number is generated regularly.
        """
        document = Document.objects.create(
            title=u'HAZOP report',
            sequencial_number="0004",
            discipline="HSE",
            document_type="REP",
            current_revision_date=u"2013-04-20",
        )
        self.assertEqual(document.document_number,
                         u'FAC09001-FWF-000-HSE-REP-0004')
        self.assertEqual(unicode(document),
                         u'FAC09001-FWF-000-HSE-REP-0004')

    def test_jsonification(self):
        """
        Tests that a jsonified document returns the appropriate values.
        """
        document = Document.objects.create(
            title=u'HAZOP report',
            sequencial_number="0004",
            discipline="HSE",
            document_type="REP",
            current_revision_date=u"2013-04-20",
            current_revision=u"01",
        )
        DocumentRevision.objects.create(
            revision=u"01",
            revision_date=u"2013-04-20",
            document=document,
        )
        self.assertEqual(
            document.jsonified(),
            {
                u'status': u'STD',
                u'favorited': False,
                u'title': u'HAZOP report',
                u'url': '/detail/FAC09001-FWF-000-HSE-REP-0004/',
                u'document_number': u'FAC09001-FWF-000-HSE-REP-0004',
                u'current_revision': u'01',
                u'number': u'FAC09001-FWF-000-HSE-REP-0004',
                u'current_revision_date': u'2013-04-20',
                u'pk': 1,
                u'favorite_id': u''
            }
        )


    def test_display_fields(self):
        """
        Tests that a document is displayed with a few fields only.
        """
        document = Document.objects.create(
            title=u'HAZOP report',
            sequencial_number="0004",
            discipline="HSE",
            document_type="REP",
            current_revision_date=u"2013-04-20",
            current_revision=u"03",
        )
        DocumentRevision.objects.create(
            revision=u"03",
            revision_date=u"2013-04-20",
            document=document,
        )
        self.assertEqual(
            u" | ".join(unicode(field[2]) for field in document.display_fields()),
            u'FAC09001-FWF-000-HSE-REP-0004 | HAZOP report | 2013-04-20 | 03 | STD'
        )