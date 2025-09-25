from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('propertyCrud', '0006_add_order_field'),
	]

	operations = [
		migrations.AddField(
			model_name='property',
			name='developer',
			field=models.CharField(max_length=255, null=True, blank=True),
		),
	]
