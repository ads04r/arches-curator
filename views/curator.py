from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, Http404
from arches.app.models import models
from arches.app.models.card import Card
from arches.app.models.graph import Graph
from arches.app.models.tile import Tile
from arches.app.views.plugin import PluginView
from arches.app.models.system_settings import settings
from arches.app.utils.betterJSONSerializer import JSONSerializer
from uuid import uuid4
from ..models import CuratedDataset
import json, datetime, pytz, urllib.parse

@method_decorator(csrf_exempt, name="dispatch")
class Curator(View):

	def serialize_datasets(self, user_id):
		res = [{'id': str(dataset.search_id), 'label': dataset.search_label, 'results': dataset.search_results_count} for dataset in CuratedDataset.objects.filter(search_user__id=user_id).exclude(search_label='').exclude(search_results_count=0)]
		return res

	def tidy_up(self):
		"""Remove all CuratedDataset objects that have no results and are over 48 hours old, to free up space and keep the database tidy."""
		CuratedDataset.objects.filter(search_results_count=0, updated_time__lte=pytz.utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(hours=48)).delete()

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

class CuratorReport(PluginView):
	def get(self, request, searchid=None):

		plugin = models.Plugin.objects.get(slug='curator')
		user = request.user
		if not user.is_authenticated:
			raise Http404()
		dataset = get_object_or_404(CuratedDataset, search_id=searchid)
		if user.id != dataset.search_user.id:
			raise Http404()
		resource_graphs = (
			models.GraphModel.objects.exclude(
				pk=settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID
			)
			.exclude(isresource=False)
			.exclude(publication=None)
		)
		widgets = models.Widget.objects.all()
		card_components = models.CardComponent.objects.all()
		datatypes = models.DDataType.objects.all()
		map_markers = models.MapMarker.objects.all()
		geocoding_providers = models.Geocoder.objects.all()
		templates = models.ReportTemplate.objects.all()
		plugins = models.Plugin.objects.all()

		context = self.get_context_data(
			plugin=plugin,
			plugin_json=JSONSerializer().serialize(plugin),
			plugins_json=JSONSerializer().serialize(plugins),
			main_script="views/plugin",
			resource_graphs=resource_graphs,
			widgets=widgets,
			widgets_json=JSONSerializer().serialize(widgets),
			card_components=card_components,
			card_components_json=JSONSerializer().serialize(card_components),
			datatypes_json=JSONSerializer().serialize(
				datatypes, exclude=["iconclass", "modulename", "classname"]
			),
			map_markers=map_markers,
			geocoding_providers=geocoding_providers,
			report_templates=templates,
			templates_json=JSONSerializer().serialize(
				templates, sort_keys=False, exclude=["name", "description"]
			),
		)

		context["nav"]["title"] = ""
		context["nav"]["menu"] = False
		context["nav"]["icon"] = plugin.icon
		context["nav"]["title"] = plugin.name

		context['dataset'] = dataset

		return render(request, "views/curator.htm", context)
