# Generated by Django 2.2.3 on 2019-07-30 08:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190730_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b78177e3-a2a7-4493-9562-46223d2cefa7')),
        ),
    ]
