# Generated by Django 2.2.13 on 2021-03-01 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0073_merge_20210104_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityentry',
            name='population',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
