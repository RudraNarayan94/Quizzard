# Generated by Django 5.0.7 on 2024-07-23 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='profile_picture',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='profile_pictures/'),
        ),
    ]
