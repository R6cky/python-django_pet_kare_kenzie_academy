# Generated by Django 4.2.4 on 2023-08-11 20:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0006_alter_pet_group_alter_pet_trait"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pet",
            old_name="trait",
            new_name="traits",
        ),
    ]
