# Generated by Django 3.0.8 on 2020-07-11 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20200711_1708'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='desctiption',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Subcategory'),
        ),
    ]
