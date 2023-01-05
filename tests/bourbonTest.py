import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from AllThingsBourbonAPI.models import BourbonStaff, Bourbon

class BourbonTests(APITestCase):

    fixtures = ['users', 'tokens', 'bourbon_staff', 'bourbons', 'bourbon_types']

    def setUp(self):
        self.bourbon_staff = BourbonStaff.objects.first()
        token = Token.objects.get(user=self.bourbon_staff.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_bourbon(self):
        """
        Ensures we can create a new bourbon
        """

        url = "/bourbons"

        data = {
            "name": "Four Roses",
            "proof": 90,
            "aroma": "it's fine",
            "taste": "also fine",
            "finish": "could be better",
            "description": "does the job",
            "made_in": "a place",
            "link_to_buy": "www.alcohol.com",
            "bourbon_img": "image.com",
            "type_of_bourbon": 1,
            "staff_member": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["name"], "Four Roses")
        self.assertEqual(json_response["proof"], 90)
        self.assertEqual(json_response["aroma"], "it's fine")
        self.assertEqual(json_response["taste"], "also fine")
        self.assertEqual(json_response["finish"], "could be better")
        self.assertEqual(json_response["description"], "does the job")
        self.assertEqual(json_response["made_in"], "a place")
        self.assertEqual(json_response["link_to_buy"], "www.alcohol.com")
        self.assertEqual(json_response["bourbon_img"], "image.com")
    
    def test_delete_bourbon(self):
        """
        Ensures we can delete an existing bourbon
        """
        bourbon = Bourbon()
        bourbon.name = "Four Roses"
        bourbon.proof = 90
        bourbon.aroma = "it's fine"
        bourbon.taste = "also fine"
        bourbon.finish = "could be better"
        bourbon.description = "does the job"
        bourbon.made_in = "a place"
        bourbon.link_to_buy = "www.alcohol.com"
        bourbon.bourbon_img = "image.com"
        bourbon.type_of_bourbon_id = 1
        bourbon.staff_member_id = 1
        bourbon.save()

        response = self.client.delete(f"/bourbons/{bourbon.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/bourbons/{bourbon.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_bourbon_returns_404(self):
        """
        Verify that delete for a bourbon that doesn't exist returns 404
        """
        response = self.client.delete(f"/bourbons/12345")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_bourbon(self):
        """
        Ensures we get an existing bourbon
        """
        bourbon = Bourbon()
        bourbon.name = "Four Roses"
        bourbon.proof = 90
        bourbon.aroma = "it's fine"
        bourbon.taste = "also fine"
        bourbon.finish = "could be better"
        bourbon.description = "does the job"
        bourbon.made_in = "a place"
        bourbon.link_to_buy = "www.alcohol.com"
        bourbon.bourbon_img = "image.com"
        bourbon.type_of_bourbon_id = 1
        bourbon.staff_member_id = 1
        bourbon.save()

        response = self.client.get(f"/bourbons/{bourbon.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "Four Roses")
        self.assertEqual(json_response["proof"], 90)
        self.assertEqual(json_response["aroma"], "it's fine")
        self.assertEqual(json_response["taste"], "also fine")
        self.assertEqual(json_response["finish"], "could be better")
        self.assertEqual(json_response["description"], "does the job")
        self.assertEqual(json_response["made_in"], "a place")
        self.assertEqual(json_response["link_to_buy"], "www.alcohol.com")
        self.assertEqual(json_response["bourbon_img"], "image.com")
    
    def test_change_bourbon(self):
        """
        Ensure we can change an existing bourbon
        """
        bourbon = Bourbon()
        bourbon.name = "Four Roses"
        bourbon.proof = 90
        bourbon.aroma = "it's fine"
        bourbon.taste = "also fine"
        bourbon.finish = "could be better"
        bourbon.description = "does the job"
        bourbon.made_in = "a place"
        bourbon.link_to_buy = "www.alcohol.com"
        bourbon.bourbon_img = "image.com"
        bourbon.type_of_bourbon_id = 1
        bourbon.staff_member_id = 1
        bourbon.save()

        data = {
            "type_of_bourbon": 2,
            "name": "Angel's Envy",
            "proof": 100,
            "aroma": "stellar",
            "taste": "rad",
            "finish": "neato",
            "description": "really does the job",
            "made_in": "a different place",
            "link_to_buy": "www.morealcohol.com",
            "bourbon_img": "anotherimage.com"
        }

        response = self.client.put(f"/bourbons/{bourbon.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/bourbons/{bourbon.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "Angel's Envy")
        self.assertEqual(json_response["proof"], 100)
        self.assertEqual(json_response["aroma"], "stellar")
        self.assertEqual(json_response["taste"], "rad")
        self.assertEqual(json_response["finish"], "neato")
        self.assertEqual(json_response["description"], "really does the job")
        self.assertEqual(json_response["made_in"], "a different place")
        self.assertEqual(json_response["link_to_buy"], "www.morealcohol.com")
        self.assertEqual(json_response["bourbon_img"], "anotherimage.com")