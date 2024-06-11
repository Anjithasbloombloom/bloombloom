# Generated by Django 5.0.3 on 2024-05-28 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0003_addeducation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addeducation',
            old_name='users',
            new_name='user_detail',
        ),
        migrations.AlterField(
            model_name='addeducation',
            name='degree',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='addeducation',
            name='school',
            field=models.TextField(blank=True, null=True),
        ),
    ]
