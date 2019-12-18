# Generated by Django 2.2.6 on 2019-12-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityentry',
            name='admin_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='communityentry',
            name='entry_name',
            field=models.CharField(default='Community_name', max_length=100),
        ),
        migrations.AddField(
            model_name='communityentry',
            name='entry_reason',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]
