# Generated by Django 4.2.16 on 2024-11-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("WearWellWardrobe", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AlterModelOptions(
            name="counts",
            options={"verbose_name_plural": "Counts"},
        ),
        migrations.RemoveField(
            model_name="page",
            name="content",
        ),
        migrations.RemoveField(
            model_name="page",
            name="url",
        ),
        migrations.AddField(
            model_name="page",
            name="content1",
            field=models.CharField(default="", max_length=8000),
        ),
        migrations.AddField(
            model_name="page",
            name="content2",
            field=models.CharField(default="", max_length=8000),
        ),
        migrations.AddField(
            model_name="page",
            name="content3",
            field=models.CharField(default="", max_length=8000),
        ),
        migrations.AddField(
            model_name="page",
            name="content4",
            field=models.CharField(default="", max_length=8000),
        ),
        migrations.AddField(
            model_name="page",
            name="deletable",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="page",
            name="img1",
            field=models.ImageField(default="", upload_to="contentPhotos/"),
        ),
        migrations.AddField(
            model_name="page",
            name="slug",
            field=models.SlugField(default=""),
        ),
        migrations.AlterField(
            model_name="page",
            name="title",
            field=models.CharField(default="Untitled", max_length=128),
        ),
    ]
