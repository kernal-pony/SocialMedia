# Generated by Django 5.1 on 2024-09-02 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Connect', '0002_blogs_model_blog_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs_model',
            name='blog_image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
