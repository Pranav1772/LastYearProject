# Generated by Django 5.0.3 on 2024-03-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfchat', '0003_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file_details',
            name='_id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
