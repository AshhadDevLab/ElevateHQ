# Generated by Django 5.1.1 on 2024-09-24 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0014_usersubscription_stripe_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='user_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
