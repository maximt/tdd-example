# Generated by Django 3.2.4 on 2021-08-13 07:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='uid',
            field=models.CharField(default=uuid.uuid4, max_length=40),
        ),
    ]
