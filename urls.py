from django.urls import re_path
from curator.views.curator import Curator

urlpatterns = [
	re_path(r"^curator/", Curator.as_view(), name="curator"),
]
