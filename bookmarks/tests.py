from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Bookmark, Tag


class TagModelTest(TestCase):
    def test_tag(self):
        tag1 = Tag(tag_name="Uni")
        tag2 = Tag(tag_name="Privat")

        self.assertIs(str(tag1), "Uni")
        self.assertIs(str(tag2), "Privat")

    def test_required_fields(self):
        tag1 = Tag()
        with self.assertRaises(ValidationError) as ve:
            tag1.full_clean()


class BookmarkModelTest(TestCase):
    def test_bookmark(self):
        tag1 = Tag(tag_name="Uni")
        tag2 = Tag(tag_name="Privat")
        tag1.save()
        tag2.save()

        bookmark1 = Bookmark(name="Testname")
        bookmark1.save()
        bookmark1.tags.add(tag1)
        bookmark1.tags.add(tag2)
        self.assertIs(len(bookmark1.tags.all()), 2)

    def test_required_fields(self):
        bookmark1 = Bookmark(name="Test")
        with self.assertRaises(ValidationError) as ve:
            bookmark1.full_clean()

        bookmark2 = Bookmark(link="Test")
        with self.assertRaises(ValidationError) as ve:
            bookmark2.full_clean()

        bookmark3 = Bookmark()
        with self.assertRaises(ValidationError) as ve:
            bookmark3.full_clean()


class BookmarkIndexViewTest(TestCase):
    def test_no_bookmarks(self):
        response = self.client.get(reverse('bookmarks:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Bookmarks found!")

    def test_tag_filter(self):
        tag = Tag.objects.create(tag_name="Uni")
        bookmark1 = Bookmark.objects.create(name="Bookmark 1", description="Test Bookmark", link="https://test.de")
        bookmark1.tags.add(tag)

        response = self.client.get(reverse('bookmarks:tag', args=(tag.id,)))
        self.assertQuerysetEqual(response.context['links'],
                                 ['<Bookmark: Bookmark 1: https://test.de>'])

    def test_bookmarks(self):
        tag = Tag.objects.create(tag_name="Uni")
        bookmark1 = Bookmark.objects.create(name="Bookmark 1", description="Test Bookmark", link="https://test.de")
        bookmark1.tags.add(tag)
        bookmark2 = Bookmark.objects.create(name="Bookmark 2", description="Test Bookmark 2", link="https://test2.de")
        bookmark2.tags.add(tag)

        response = self.client.get(reverse('bookmarks:index'))

        self.assertQuerysetEqual(list(response.context['links']),
                                 ['<Bookmark: Bookmark 1: https://test.de>',
                                  '<Bookmark: Bookmark 2: https://test2.de>'])

    def test_search_field(self):
        tag = Tag.objects.create(tag_name="Uni")
        bookmark1 = Bookmark.objects.create(name="Bookmark 1", description="Test Bookmark", link="https://test.de")
        bookmark1.tags.add(tag)
        bookmark2 = Bookmark.objects.create(name="Bookmark 2", description="Test Website", link="https://test2.de")
        bookmark2.tags.add(tag)

        response = self.client.post(reverse('bookmarks:index'), {'search': 'Test Bookmark'})
        self.assertQuerysetEqual(list(response.context['links']),
                                 ['<Bookmark: Bookmark 1: https://test.de>'])

        response = self.client.post(reverse('bookmarks:index'), {'search': 'Bookmark'})
        self.assertQuerysetEqual(list(response.context['links']),
                                 ['<Bookmark: Bookmark 1: https://test.de>',
                                  '<Bookmark: Bookmark 2: https://test2.de>'])

    def test_create(self):
        response = self.client.post(reverse('bookmarks:create'), {'name': 'Testname', 'link': 'https://test.de',
                                                                  'description': 'Test description'})
        self.assertQuerysetEqual(response.context['links'],
                                 ['<Bookmark: Testname: https://test.de>'])

    def test_delete(self):
        bookmark1 = Bookmark.objects.create(name="Bookmark 1", description="Test Bookmark", link="https://test.de")
        bookmark1.save()
        response = self.client.get(reverse('bookmarks:delete_bookmark', args=(bookmark1.id,)))
        self.assertQuerysetEqual(response.context['links'], [])

    def test_archive(self):
        bookmark1 = Bookmark.objects.create(name="Bookmark 1", description="Test Bookmark", link="https://test.de")
        bookmark1.save()

        response = self.client.get(reverse('bookmarks:index'))
        self.assertQuerysetEqual(response.context['links'],
                                 ['<Bookmark: Bookmark 1: https://test.de>'])

        response = self.client.get(reverse('bookmarks:archive_bookmark', args=(bookmark1.id,)))
        self.assertQuerysetEqual(response.context['links'],
                                 ['<Bookmark: Bookmark 1: https://test.de>'])

        response = self.client.get(reverse('bookmarks:index'))
        self.assertContains(response, "No Bookmarks found!")
