# Generated by Django 4.0 on 2022-02-14 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('general', '0026_excelfile_updatedate_excelfolder_updatedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excelfile',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='excelfolder',
            name='UID',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='excelfolder',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='excelfolder',
            name='tableName',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='excelfolder',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
