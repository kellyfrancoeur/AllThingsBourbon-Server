import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from AllThingsBourbonAPI.models import bourbon_user, cocktail_tried
 

class CocktailsTriedTests(APITestCase):

    fixtures = ['users', 'tokens', 'bourbon_users', 'cocktails_tried']

    def setUp(self):
        self.bourbon_user = bourbon_user.objects.first()
        token = Token.objects.get(user=self.bourbon_user.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_cocktails_tried(self):
        """
        Ensure we can get an existing cocktails tried.
        """

        Cocktail_tried = cocktail_tried()
        Cocktail_tried.cocktail = 'Manhattan'
        Cocktail_tried.comments = 'Delicious'
        Cocktail_tried.rating = '5'
        Cocktail_tried.save()

        response = self.client.get(f"/cocktailstried/{Cocktail_tried.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['cocktail'], 'Manhattan')
        self.assertEqual(json_response['comments'], 'Delicious')
        self.assertEqual(json_response['rating'], '5')

    def test_create_cocktail_tried(self):
        """
        Ensure we can create a new tried cocktail.
        """
        
        url = "/cocktailstried"
        data = {
            'cocktail': 'Old Fashioned',
            'comments': 'Second Favorite',
            'rating': '4'
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['cocktail'], 'Old Fashioned')
        self.assertEqual(json_response['comments'], 'Second Favorite')
        self.assertEqual(json_response['rating'], '4')

    def test_change_cocktail_tried(self):
        """
        Ensure we can change an existing tried cocktail.
        """
        Cocktail_tried = cocktail_tried()
        Cocktail_tried.cocktail = 'Sazerac'
        Cocktail_tried.comments = 'Did not like'
        Cocktail_tried.rating = '1'
        Cocktail_tried.save()

        data = {
            'cocktail': 'Sazerac',
            'comments': 'It was not that bad',
            'rating': '2'
        }

        response = self.client.put(f"/cocktailstried/{Cocktail_tried.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/cocktailstried/{Cocktail_tried.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['cocktail'], 'Sazerac')
        self.assertEqual(json_response['comments'], 'It was not that bad')
        self.assertEqual(json_response['rating'], '2')

    def test_delete_cocktail_tried(self):
        """
        Ensure we can delete an existing tried cocktail.
        """
        Cocktail_tried = cocktail_tried()
        Cocktail_tried.cocktail = 'Brown Derby'
        Cocktail_tried.comments = 'It was fine'
        Cocktail_tried.rating = '3'
        Cocktail_tried.save()

        response = self.client.delete(f"/cocktailstried/{Cocktail_tried.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/cocktailstried/{Cocktail_tried.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)