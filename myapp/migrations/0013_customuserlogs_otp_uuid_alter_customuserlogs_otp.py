# Generated by Django 5.0.6 on 2024-08-20 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_customuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuserlogs',
            name='otp_uuid',
            field=models.CharField(default='jgjgj', max_length=300),
        ),
        migrations.AlterField(
            model_name='customuserlogs',
            name='otp',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
