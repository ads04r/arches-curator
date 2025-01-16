from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from uuid import uuid4
from ..models import CuratedDataset
import json

@method_decorator(csrf_exempt, name="dispatch")
class Curator(View):

	def serialize_datasets(self, user_id):
		res = [{'id': str(dataset.search_id), 'label': dataset.search_label, 'results': dataset.search_results_count} for dataset in CuratedDataset.objects.filter(search_user__id=user_id).exclude(search_label='')]
		return res

	def tidy_up(self):
		return 0

	def get(self, request):
		user = request.user
		if not user.is_authenticated:
			return JsonResponse({"datasets": []})
		data = {"datasets": self.serialize_datasets(user.id)}
		return JsonResponse(data)

	def post(self, request):
		user = request.user
		if not user.is_authenticated:
			return JsonResponse({"id": "", "datasets": []})
		request_data = json.loads(request.body)
		if len(request_data['id']) == 0:
			ret = CuratedDataset(search_user=user, search_id=uuid4(), search_results_count=0)
		else:
			ret = get_object_or_404(CuratedDataset, search_id=request_data['id'])
		if user.id != ret.search_user.id:
			raise Http404()
		if 'title' in request_data:
			if len(request_data['title']) > 0:
				ret.search_label = request_data['title']
		if 'results' in request_data:
			ret.search_results = int(request_data['results'])
		if 'url' in request_data:
			if len(request_data['url']) > 0:
				ret.search_url = request_data['url']
		if 'geojson' in request_data:
			if len(request_data['geojson']) > 0:
				ret.search_results = {"search_url": request_data['geojson'], "features": [], "type": "FeatureCollection"}
		ret.save()

		data = {"id": ret.search_id, "datasets": self.serialize_datasets(user.id)}
		return JsonResponse(data)

