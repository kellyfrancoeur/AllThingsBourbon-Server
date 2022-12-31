import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from AllThingsBourbonAPI.models import bourbon_user, distillery_visited


class DistilleryVisitedTests(APITestCase):

    fixtures = ['users', 'tokens', 'bourbon_users', 'distilleries_visited']

    def setUp(self):
        self.bourbon_user = bourbon_user.objects.first()
        token = Token.objects.get(user=self.bourbon_user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_distilleries_visited(self):
        """
        Ensure we can get an existing distilleries visited.
        """

        Distillery_visited = distillery_visited()
        Distillery_visited.distillery = '45th Parallel Spirits'
        Distillery_visited.comments = 'It was cool'
        Distillery_visited.rating = '3'
        Distillery_visited.save()

        response = self.client.get(f"/distilleriesvisited/{Distillery_visited.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['distillery'], '45th Parallel Spirits')
        self.assertEqual(json_response['comments'], 'It was cool')
        self.assertEqual(json_response['rating'], '3')

    def test_create_distillery_visited(self):
        """
        Ensure we can create a new distillery visited.
        """
        
        url = "/distilleriesvisited"
        data = {
            'distillery': 'Alamo Distilling Co.',
            'comments': 'It was ok',
            'rating': '2'
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['distillery'], 'Alamo Distilling Co.')
        self.assertEqual(json_response['comments'], 'It was ok')
        self.assertEqual(json_response['rating'], '2')

    def test_change_distillery_visited(self):
        """
        Ensure we can change an existing distillery visited.
        """
        Distillery_visited = distillery_visited()
        Distillery_visited.distillery = 'Amador Distillery'
        Distillery_visited.comments = 'It was great'
        Distillery_visited.rating = '5'
        Distillery_visited.save()

        data = {
            'distillery': 'Amador Distillery',
            'comments': 'It was pretty great',
            'rating': '4'
        }

        response = self.client.put(f"/distilleriesvisited/{Distillery_visited.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/distilleriesvisited/{Distillery_visited.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['distillery'], 'Amador Distillery')
        self.assertEqual(json_response['comments'], 'It was pretty great')
        self.assertEqual(json_response['rating'], '4')

    def test_delete_distillery_visited(self):
        """
        Ensure we can delete an existing distillery visited.
        """
        Distillery_visited = distillery_visited()
        Distillery_visited.distillery = 'Amador Distillery'
        Distillery_visited.comments = 'It was pretty great'
        Distillery_visited.rating = '4'
        Distillery_visited.save()

        response = self.client.delete(f"/distilleriesvisited/{Distillery_visited.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/distilleriesvisited/{Distillery_visited.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)