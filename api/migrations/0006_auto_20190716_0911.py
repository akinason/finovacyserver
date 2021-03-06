# Generated by Django 2.2.3 on 2019-07-16 09:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190713_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='borrower_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='branch_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='submitted_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
