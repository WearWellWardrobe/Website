# Generated by Django 4.2.16 on 2024-11-13 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WearWellWardrobe", "0004_page_displaystyle"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="pageNotes",
            field=models.CharField(blank=True, default="", max_length=4096, null=True),
        ),
    ]
