import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from AllThingsBourbonAPI.models import BourbonStaff, Cocktail

class CocktailTests(APITestCase):

    fixtures = ['users', 'tokens', 'bourbon_staff', 'cocktails', 'cocktail_types']

    def setUp(self):
        self.bourbon_staff = BourbonStaff.objects.first()
        token = Token.objects.get(user=self.bourbon_staff.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_cocktail(self):
        """
        Ensures we can create a new cocktail
        """

        url = "/cocktails"

        data = {
            "name": "Manhattan",
            "ingredients": "some stuff",
            "how_to_make": "shake it up",
            "cocktail_img": "image.com",
            "type_of_cocktail": 1,
            "staff_member": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["name"], "Manhattan")
        self.assertEqual(json_response["ingredients"], "some stuff")
        self.assertEqual(json_response["how_to_make"], "shake it up")
        self.assertEqual(json_response["cocktail_img"], "image.com")
    
    def test_delete_cocktail(self):
        """
        Ensures we can delete an existing cocktail
        """
        cocktail = Cocktail()
        cocktail.name = "Manhattan"
        cocktail.ingredients = "some stuff"
        cocktail.how_to_make = "shake it up"
        cocktail.cocktail_img = "image.com"
        cocktail.type_of_cocktail_id = 1
        cocktail.staff_member_id = 1
        cocktail.save()

        response = self.client.delete(f"/cocktails/{cocktail.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/cocktails/{cocktail.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_cocktail_returns_404(self):
        """
        Verify that delete for a cocktail that doesn't exist returns 404
        """
        response = self.client.delete(f"/cocktails/12345")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_cocktail(self):
        """
        Ensures we get an existing cocktail
        """
        cocktail = Cocktail()
        cocktail.name = "Manhattan"
        cocktail.ingredients = "some stuff"
        cocktail.how_to_make = "shake it up"
        cocktail.cocktail_img = "image.com"
        cocktail.type_of_cocktail_id = 1
        cocktail.staff_member_id = 1
        cocktail.save()

        response = self.client.get(f"/cocktails/{cocktail.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "Manhattan")
        self.assertEqual(json_response["ingredients"], "some stuff")
        self.assertEqual(json_response["how_to_make"], "shake it up")
        self.assertEqual(json_response["cocktail_img"], "image.com")
    
    def test_change_cocktail(self):
        """
        Ensure we can change an existing cocktail
        """
        cocktail = Cocktail()
        cocktail.name = "Manhattan"
        cocktail.ingredients = "some stuff"
        cocktail.how_to_make = "shake it up"
        cocktail.cocktail_img = "image.com"
        cocktail.type_of_cocktail_id = 1
        cocktail.staff_member_id = 1
        cocktail.save()

        data = {
            "type_of_cocktail": 2,
            "name": "Old Fashioned",
            "ingredients": "more stuff",
            "how_to_make": "stir it up",
            "cocktail_img": "anotherimage.com"
        }

        response = self.client.put(f"/cocktails/{cocktail.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/cocktails/{cocktail.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "Old Fashioned")
        self.assertEqual(json_response["ingredients"], "more stuff")
        self.assertEqual(json_response["how_to_make"], "stir it up")
        self.assertEqual(json_response["cocktail_img"], "anotherimage.com")