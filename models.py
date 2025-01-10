from django.db import models
from django.contrib.auth.models import User

class CuratedDataset(models.Model):
	"""This is a class representing a curated dataset, which is effectively a saved search
	that a user can create. It keeps a record of the search performed, which user performed
	the search and when, as well as a GeoJSON representation of the results, because these
	may change if the user or time is different."""
	search_id = models.UUIDField(primary_key=True)
	search_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='curated_datasets')
	search_url = models.URLField()
	"""The URL called in order to instigate this search."""
	search_results = models.JSONField(default='{}')
	"""A GeoJSON object representing the results of this search, as they would have been presented to the user."""
	created_time = models.DateTimeField(auto_now_add=True)
	"""A datetime representing the time this Event object was created."""
	updated_time = models.DateTimeField(auto_now=True)
	"""A datetime representing the time this Event object was last modified."""

	class Meta:

		db_table = "curated_dataset"
		managed = False
		verbose_name = 'curated dataset'
		verbose_name_plural = 'curated datasets'
