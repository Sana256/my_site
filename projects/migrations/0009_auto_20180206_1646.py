# Generated by Django 2.0.1 on 2018-02-06 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20180206_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='projects.Project'),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(),
        ),
    ]