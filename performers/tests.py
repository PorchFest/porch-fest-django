from django.core.exceptions import ValidationError
from django.test            import TestCase

from .models                import Genre, Performer


class PerformerSlugTests(TestCase):
    def test_slug_is_generated_from_name(self):
        performer = Performer.objects.create(name="The Olives")
        self.assertEqual(performer.slug, "the-olives")

    def test_duplicate_names_get_distinct_slugs(self):
        Performer.objects.create(name="The Olives")
        second = Performer.objects.create(name="The Olives")
        self.assertEqual(second.slug, "the-olives-1")

    def test_existing_slug_is_kept(self):
        performer = Performer.objects.create(name="The Olives", slug="olives")
        self.assertEqual(performer.slug, "olives")


class GenreSlugTests(TestCase):
    def test_slug_is_generated_from_name(self):
        genre = Genre.objects.create(name="Singer Songwriter")
        self.assertEqual(genre.slug, "singer-songwriter")

    def test_duplicate_slug_is_rejected(self):
        Genre.objects.create(name="Rock")
        with self.assertRaises(ValidationError):
            Genre.objects.create(name="Rock")
