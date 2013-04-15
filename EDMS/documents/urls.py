from django.conf.urls import patterns, url

from documents.views import (
    DocumentList, DocumentFilter, DocumentCreate
)

urlpatterns = patterns(
    '',
    url(r'^filter/$',
        DocumentFilter.as_view(),
        name="document_filter"),
    url(r'^create/$',
        DocumentCreate.as_view(),
        name="document_create"),
    url(r'^$',
        DocumentList.as_view(),
        name="document_list"),
)