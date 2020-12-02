# Generated by Django 2.2.13 on 2020-10-23 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0057_auto_20201023_0846"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communityentry",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="submissions",
                to="main.Organization",
            ),
        ),
    ]