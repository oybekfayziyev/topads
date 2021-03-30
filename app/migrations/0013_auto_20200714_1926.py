# Generated by Django 3.0.8 on 2020-07-14 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_auto_20200714_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dislike',
            name='product',
        ),
        migrations.AddField(
            model_name='dislike',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='user',
        ),
        migrations.AddField(
            model_name='dislike',
            name='user',
            field=models.ManyToManyField(related_name='dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='like',
            name='product',
        ),
        migrations.AddField(
            model_name='like',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Product'),
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Subcategory'),
        ),
    ]