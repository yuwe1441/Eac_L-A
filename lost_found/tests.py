from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Claim, Item


class ModerationFlowTests(TestCase):
	def setUp(self):
		self.admin = User.objects.create_user(username='admin', password='secret123', is_staff=True)

	def test_anonymous_lost_report_requires_approval(self):
		response = self.client.post(reverse('report_lost'), {
			'name': 'Guest User',
			'contact': 'guest@example.com',
			'title': 'Missing Wallet',
			'category': 'Personal Effects',
			'location': 'Cafeteria',
			'description': 'Black leather wallet',
			'date_lost': '2026-03-01',
			'time_lost': '10:00',
		})

		self.assertEqual(response.status_code, 302)
		item = Item.objects.get(title='Missing Wallet')
		self.assertEqual(item.moderation_status, 'pending')
		self.assertEqual(Item.objects.filter(moderation_status='approved').count(), 0)

	def test_admin_lost_report_is_auto_approved(self):
		self.client.login(username='admin', password='secret123')
		self.client.post(reverse('report_lost'), {
			'name': 'OSA Staff',
			'contact': 'osa@example.com',
			'title': 'Student ID',
			'category': 'Documents',
			'location': 'OSA Office',
			'description': 'Turned in at OSA',
			'date_lost': '2026-03-01',
			'time_lost': '09:30',
		})

		item = Item.objects.get(title='Student ID')
		self.assertEqual(item.moderation_status, 'approved')
		self.assertEqual(item.reviewed_by, self.admin)

	def test_anonymous_found_report_requires_approval(self):
		response = self.client.post(reverse('report_found'), {
			'name': 'Helpful Finder',
			'contact': 'finder@example.com',
			'title': 'Calculator',
			'category': 'Electronics',
			'location': 'Engineering Building',
			'description': 'Scientific calculator in a black case',
			'date_found': '2026-03-02',
			'time_found': '13:15',
			'is_surrendered_to_osa': 'on',
		})

		self.assertEqual(response.status_code, 302)
		item = Item.objects.get(title='Calculator')
		self.assertEqual(item.status, 'Found')
		self.assertEqual(item.moderation_status, 'pending')
		self.assertTrue(item.is_surrendered_to_osa)

	def test_admin_found_report_is_auto_approved_and_marked_at_osa(self):
		self.client.login(username='admin', password='secret123')
		self.client.post(reverse('report_found'), {
			'name': 'OSA Desk',
			'contact': 'Desk intake',
			'title': 'Gray Jacket',
			'category': 'Personal Effects',
			'location': 'OSA Office',
			'description': 'Claim tag attached at the counter',
			'date_found': '2026-03-02',
			'time_found': '14:45',
		})

		item = Item.objects.get(title='Gray Jacket')
		self.assertEqual(item.status, 'Found')
		self.assertEqual(item.moderation_status, 'approved')
		self.assertTrue(item.is_surrendered_to_osa)
		self.assertEqual(item.reviewed_by, self.admin)

	def test_claim_request_requires_admin_approval(self):
		item = Item.objects.create(
			title='Phone',
			category='Electronics',
			status='Found',
			moderation_status='approved',
			location='Library',
			description='Blue phone',
		)

		response = self.client.post(reverse('claim_item'), {
			'item_id': item.id,
			'name': 'Claimant',
			'contact': 'claimant@example.com',
			'reason': 'It has my wallpaper and case.',
		})

		self.assertEqual(response.status_code, 302)
		claim = Claim.objects.get(item=item)
		self.assertEqual(claim.status, 'pending')

	def test_claim_request_without_item_redirects_safely(self):
		response = self.client.post(reverse('claim_item'), {
			'item_id': '',
			'name': 'Claimant',
			'contact': 'claimant@example.com',
			'reason': 'It is mine.',
		})

		self.assertEqual(response.status_code, 302)
		self.assertEqual(Claim.objects.count(), 0)

	def test_admin_can_approve_claim(self):
		item = Item.objects.create(
			title='Phone',
			category='Electronics',
			status='Found',
			moderation_status='approved',
			location='Library',
			description='Blue phone',
		)
		claim = Claim.objects.create(
			item=item,
			claimant_name='Claimant',
			claimant_contact='claimant@example.com',
			reason='It is mine.',
		)

		self.client.login(username='admin', password='secret123')
		response = self.client.post(reverse('approve_claim', args=[claim.id]))

		self.assertEqual(response.status_code, 302)
		claim.refresh_from_db()
		self.assertEqual(claim.status, 'approved')
		self.assertEqual(claim.reviewed_by, self.admin)

	def test_item_detail_shows_osa_release_message_for_surrendered_found_items(self):
		item = Item.objects.create(
			title='Umbrella',
			category='Others',
			status='Found',
			moderation_status='approved',
			location='Main Lobby',
			description='Black folding umbrella',
			is_surrendered_to_osa=True,
		)

		response = self.client.get(reverse('item_detail', args=[item.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Claim Through OSA')
		self.assertContains(response, 'Visit OSA directly or submit a claim request here for verification.')

	def test_admin_can_open_pending_item_detail(self):
		item = Item.objects.create(
			title='Pending Headphones',
			category='Electronics',
			status='Found',
			moderation_status='pending',
			location='Gym',
			description='Black over-ear headphones',
		)

		self.client.login(username='admin', password='secret123')
		response = self.client.get(reverse('item_detail', args=[item.id]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Pending')
		self.assertContains(response, 'Back to Listings')
		self.assertContains(response, 'Lost Item Reports')
