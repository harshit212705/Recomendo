# Generated by Django 3.2.7 on 2021-10-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recommender', '0008_userinteresttags'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(default=20),
        ),
    ]
