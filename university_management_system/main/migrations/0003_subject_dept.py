# Generated by Django 3.1.7 on 2021-12-08 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211208_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.dept'),
            preserve_default=False,
        ),
    ]
