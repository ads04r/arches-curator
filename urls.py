from django.urls import re_path
from django.conf import settings
from curator.views.curator import Curator, CuratorReport

uuid_regex = settings.UUID_REGEX

urlpatterns = [
	re_path(r"^curator/(?P<searchid>%s)$" % uuid_regex, CuratorReport.as_view(), name="curator_report"),
	re_path(r"^curator/", Curator.as_view(), name="curator")
]

