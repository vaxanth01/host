# Generated by Django 4.2 on 2024-10-09 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account'),
        ),
    ]
