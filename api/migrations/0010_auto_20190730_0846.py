# Generated by Django 2.2.3 on 2019-07-30 08:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20190730_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ba82523c-8d33-4735-bd68-f9b1ee81cce7')),
        ),
    ]
