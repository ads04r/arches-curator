from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

	dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('curator', '0001_initial')]

	operations = [
		migrations.CreateModel(
			name='CuratedDataset',
			fields=[
				('search_id', models.UUIDField(primary_key=True, serialize=False)),
				('search_url', models.URLField(max_length=2048)),
				('search_results', models.JSONField(default='{}')),
				('created_time', models.DateTimeField(auto_now_add=True)),
				('updated_time', models.DateTimeField(auto_now=True)),
				('search_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curated_datasets', to=settings.AUTH_USER_MODEL))
			],
			options={
				'verbose_name': 'curated dataset',
				'verbose_name_plural': 'curated datasets',
				'db_table': 'curated_dataset',
				'managed': True
			}
		)
	]
