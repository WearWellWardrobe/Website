# Generated by Django 2.1.5 on 2025-01-05 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WearWellWardrobe', '0005_page_pagenotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='id',
        ),
        migrations.AddField(
            model_name='page',
            name='page_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
