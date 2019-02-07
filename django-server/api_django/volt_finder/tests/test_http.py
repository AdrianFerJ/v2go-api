from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

PASSWORD = 'pAssw0rd!'

""" HELPER FUNC """
def create_user(username='user@example.com', password=PASSWORD): # new
    return get_user_model().objects.create_user(
        username=username, password=password)


""" TESTS """

class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    # Function collapsed for clarity.
    def test_user_can_sign_up(self): ...

    def test_user_can_log_in(self): # new
        user = create_user()
        response = self.client.post(reverse('log_in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self): # new
        user = create_user()
        self.client.login(username=user.username, password=PASSWORD)
        response = self.client.post(reverse('log_out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)