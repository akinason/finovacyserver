# Generated by Django 2.2.3 on 2019-07-30 15:17

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20190730_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='return_url',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9b0ab823-cd79-4427-af68-2af29518aa17')),
        ),
    ]
