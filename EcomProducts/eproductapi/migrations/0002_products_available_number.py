# Generated by Django 4.0.6 on 2023-03-07 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eproductapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='available_number',
            field=models.PositiveIntegerField(default=1),
        ),
    ]