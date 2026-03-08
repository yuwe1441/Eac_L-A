from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lost_found', '0004_item_moderation_claim'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_surrendered_to_osa',
            field=models.BooleanField(default=False),
        ),
    ]