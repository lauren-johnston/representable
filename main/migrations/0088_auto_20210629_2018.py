# Generated by Django 2.2.20 on 2021-06-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0087_communityentry_test"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="communityentry",
            name="test",
        ),
        migrations.AddField(
            model_name="communityentry",
            name="community_hash",
            field=models.CharField(default="", max_length=256),
        ),
    ]
