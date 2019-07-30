# Generated by Django 2.2.3 on 2019-07-12 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190712_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.IntegerField(blank=True, null=True)),
                ('savings_id', models.IntegerField(blank=True, null=True)),
                ('transaction_date', models.DateField(blank=True, null=True)),
                ('transaction_time', models.TimeField(blank=True, null=True)),
                ('transaction_type_id', models.IntegerField(blank=True, null=True)),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('transaction_description', models.CharField(blank=True, max_length=255)),
                ('transaction_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=50)),
                ('borrower_mobile', models.CharField(blank=True, max_length=50)),
                ('server_transaction_status', models.CharField(blank=True, max_length=20)),
                ('is_completed', models.BooleanField(default=False)),
                ('third_party_reference', models.CharField(blank=True, max_length=255)),
                ('third_party_immediate_response', models.TextField(blank=True)),
                ('third_party_callback_response', models.TextField(blank=True)),
                ('server_transaction_type', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]