# Generated by Django 2.2.3 on 2019-07-12 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
