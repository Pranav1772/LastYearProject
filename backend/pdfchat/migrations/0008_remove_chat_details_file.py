# Generated by Django 5.0.3 on 2024-03-11 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pdfchat', '0007_chat_details_assistant_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat_details',
            name='file',
        ),
    ]