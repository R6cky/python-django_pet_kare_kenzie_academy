# Generated by Django 4.2.4 on 2023-08-17 01:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0003_rename_name_trait_trait_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trait",
            old_name="trait_name",
            new_name="name",
        ),
    ]
