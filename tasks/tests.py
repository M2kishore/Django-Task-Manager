from selectors import EVENT_READ
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from .views import GenericTaskView

from tasks.models import Task

from task_manager.celery import every_30_seconds

USER_NAME = "bruce_wayne"
USER_PASSWORD = "i_am_batman"


class QuestionModelTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=USER_NAME, email="bruce@wayne.org", password=USER_PASSWORD
        )

    def test_authenticated(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        # Create an instance of a GET request.
        request = self.factory.get("/tasks")
        # Set the user instance on the request.
        request.user = self.user
        # We simply create the view and call it like a regular function
        response = GenericTaskView.as_view()(request)
        # Since we are authenticated we get a 200 response
        self.assertEqual(response.status_code, 200)

    def test_celery(self):
        celery_response = every_30_seconds()
        self.assertEqual(celery_response, True)