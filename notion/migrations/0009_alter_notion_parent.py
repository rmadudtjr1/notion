# Generated by Django 5.0.6 on 2024-05-31 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notion', '0008_alter_notion_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notion',
            name='parent',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
    ]
