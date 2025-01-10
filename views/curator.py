from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from arches.app.models.models import ResourceInstance, TileModel
from django.http import JsonResponse
from ..models import CuratedDataset

@method_decorator(csrf_exempt, name="dispatch")
class Curator(View):

	def serialize_datasets(self, user_id):
		res = [{'id': str(dataset.search_id), 'label': dataset.search_label, 'results': dataset.search_results_count} for dataset in CuratedDataset.objects.filter(search_user__id=user_id)]
		return res

	def get(self, request):
		user = request.user
		if not user.is_authenticated:
			return JsonResponse({"datasets": []})
		data = {"records": self.serialize_datasets(user.id)}
		return JsonResponse(data)

	def post(self, request):
		state = {
			"resources": ResourceInstance.objects.count(),
			"tiles": TileModel.objects.count()
		}
		data = {"records": self.serialize_datasets()}
		return JsonResponse(data)

