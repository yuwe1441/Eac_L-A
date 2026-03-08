from django.core.management.base import BaseCommand

from lost_found.models import Claim, Item


class Command(BaseCommand):
    help = "Delete all lost/found items and claim records (does not delete users)."

    def handle(self, *args, **options):
        item_count = Item.objects.count()
        claim_count = Claim.objects.count()

        if item_count == 0 and claim_count == 0:
            self.stdout.write(self.style.SUCCESS('No items or claims to delete.'))
            return

        Item.objects.all().delete()
        Claim.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deleted {item_count} item(s) and {claim_count} claim(s)."
        ))
