# Generated by Django 2.1.5 on 2020-04-02 11:55

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0029_remove_profile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=website.models.Profile.get_file_path),
        ),
    ]