# Generated by Django 5.0.3 on 2024-03-11 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfchat', '0006_chat_details_openai_file_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat_details',
            name='assistant_id',
            field=models.CharField(default='assistantid', max_length=255),
        ),
        migrations.AlterField(
            model_name='chat_details',
            name='openai_file_id',
            field=models.CharField(default='fileid', max_length=255),
        ),
    ]
