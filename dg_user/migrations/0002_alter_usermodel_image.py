# Generated by Django 4.2.5 on 2023-10-12 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dg_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='image',
            field=models.ImageField(null=True, upload_to='Uploaded Files/'),
        ),
    ]