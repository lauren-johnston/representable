# Generated by Django 2.2.20 on 2021-06-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0086_merge_20210617_1455"),
    ]

    operations = [
        migrations.AddField(
            model_name="communityentry",
            name="test",
            field=models.CharField(blank=True, max_length=64),
        ),
    ]