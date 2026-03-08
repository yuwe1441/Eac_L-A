from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    STATUS_CHOICES = [('Lost', 'Lost'), ('Found', 'Found')]
    MODERATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Documents', 'Documents'),
        ('Personal Effects', 'Personal Belongings'),
        ('Others', 'Others'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    moderation_status = models.CharField(max_length=10, choices=MODERATION_STATUS_CHOICES, default='pending')
    location = models.CharField(max_length=200)
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)
    date_lost = models.DateField(null=True, blank=True)
    time_lost = models.TimeField(null=True, blank=True)
    reporter_name = models.CharField(max_length=120, blank=True)
    reporter_contact = models.CharField(max_length=120, blank=True)
    is_surrendered_to_osa = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_items')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_visible(self):
        return self.moderation_status == 'approved'

    @property
    def reporter_display_name(self):
        if self.reporter_name:
            return self.reporter_name
        if self.user:
            return self.user.username
        return 'Anonymous'

    @property
    def incident_label(self):
        return 'Date Found' if self.status == 'Found' else 'Date Lost'

    @property
    def contact_label(self):
        if self.status == 'Found' and self.is_surrendered_to_osa:
            return 'Claim Through OSA'
        return 'Reporter Contact'

    @property
    def public_contact_display(self):
        if self.status == 'Found' and self.is_surrendered_to_osa:
            return 'This item is already with the OSA office. Visit OSA directly or submit a claim request here for verification.'
        return self.reporter_contact or 'No contact details were provided.'

    def __str__(self):
        return f"{self.status}: {self.title}"


class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant_name = models.CharField(max_length=120)
    claimant_contact = models.CharField(max_length=120)
    reason = models.TextField()
    image = models.ImageField(upload_to='claims/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claims')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_claims')
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.item.title} claim by {self.claimant_name}"
