from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lost_found', '0003_item_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='moderation_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='item',
            name='reporter_contact',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='item',
            name='reporter_name',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='item',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claimant_name', models.CharField(max_length=120)),
                ('claimant_contact', models.CharField(max_length=120)),
                ('reason', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='claims/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='lost_found.item')),
                ('reviewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_claims', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='claims', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]