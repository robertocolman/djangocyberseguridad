# Generated by Django 5.1.1 on 2024-10-16 21:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comentario_fch_creado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fch_creado',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 16, 21, 28, 10, 938169, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 16, 21, 28, 10, 937018, tzinfo=datetime.timezone.utc)),
        ),
    ]
