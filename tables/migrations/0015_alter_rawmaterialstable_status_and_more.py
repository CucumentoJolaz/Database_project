# Generated by Django 4.0 on 2022-02-11 18:22

from django.db import migrations, models
import django.db.models.deletion
import tables.models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0014_alter_rawmaterialstable_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterialstable',
            name='status',
            field=models.ForeignKey(default=tables.models.statusTable.getDefaultPk, on_delete=django.db.models.deletion.SET_DEFAULT, to='tables.statustable'),
        ),
        migrations.AlterField(
            model_name='subcomponentstable',
            name='status',
            field=models.ForeignKey(default=tables.models.statusTable.getDefaultPk, on_delete=django.db.models.deletion.SET_DEFAULT, to='tables.statustable'),
        ),
    ]