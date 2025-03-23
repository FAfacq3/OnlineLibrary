from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from library.models import Material, UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.material = Material.objects.create(
            title="Test Material",
            description="Test Description",
            category="Book",
            uploaded_by=self.user,
            file=SimpleUploadedFile("testfile.txt", b"Test content")
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/home.html')

    def test_material_list_view(self):
        response = self.client.get(reverse('material_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Material')

    def test_material_detail_view(self):
        response = self.client.get(reverse('material_detail', args=[self.material.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Description')

    def test_dashboard_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'library/dashboard.html')