from django.test import RequestFactory
from arches.app.views.api import SearchExport
import json

def local_api_search(url, user):

	rf = RequestFactory()
	view = SearchExport.as_view()
	r = rf.get(url)
	r.user = user

	try:
		return json.loads(view(r).content)
	except:
		return {}
