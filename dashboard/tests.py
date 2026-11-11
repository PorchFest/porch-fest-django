from datetime                   import time

from django.contrib.auth.models import User
from django.test                import TestCase

from performers.models          import Performer
from porches.models             import Performance, Porch
from .models                    import Request


class RequestAcceptedTests(TestCase):
    def test_accepting_a_request_creates_the_performance(self):
        user = User.objects.create_user("host")
        porch = Porch.objects.create(
            name="Blue Porch",
            owner_name="Host",
            owner_email="host@example.com",
            street_address="123 Olive Ave",
        )
        performer = Performer.objects.create(name="The Olives", slug="the-olives")
        request = Request.objects.create(
            porch=porch, performer=performer, requested_by=user,
            start_time=time(13, 0), end_time=time(13, 45),
        )
        self.assertFalse(Performance.objects.exists())

        request.status = "accepted"
        request.save()

        performance = Performance.objects.get()
        self.assertEqual(performance.porch, porch)
        self.assertEqual(performance.performer, performer)
        self.assertEqual(performance.created_by, user)
        self.assertEqual(performance.start_time, time(13, 0))
