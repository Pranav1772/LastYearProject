# Generated by Django 5.0.3 on 2024-03-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PDF_Details',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
    ]