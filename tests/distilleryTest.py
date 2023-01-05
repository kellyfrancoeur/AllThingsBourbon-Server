import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from AllThingsBourbonAPI.models import BourbonStaff, Distillery

class DistilleryTests(APITestCase):

    fixtures = ['users', 'tokens', 'bourbon_staff', 'distilleries']

    def setUp(self):
        self.bourbon_staff = BourbonStaff.objects.first()
        token = Token.objects.get(user=self.bourbon_staff.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_distillery(self):
        """
        Ensures we can create a new distillery
        """

        url = "/distilleries"

        data = {
            "name": "Corsair",
            "location": "some place",
            "description": "it makes bourbon",
            "link_to_site": "www.somewhere.com",
            "distillery_img": "image.com",
            "staff_member": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["name"], "Corsair")
        self.assertEqual(json_response["location"], "some place")
        self.assertEqual(json_response["description"], "it makes bourbon")
        self.assertEqual(json_response["link_to_site"], "www.somewhere.com")
        self.assertEqual(json_response["distillery_img"], "image.com")
    
    def test_delete_distillery(self):
        """
        Ensures we can delete an existing distillery
        """
        distillery = Distillery()
        distillery.name = "Corsair"
        distillery.location = "some place"
        distillery.description = "it makes bourbon"
        distillery.link_to_site = "www.somewhere.com"
        distillery.distillery_img = "image.com"
        distillery.staff_member_id = 1
        distillery.save()

        response = self.client.delete(f"/distilleries/{distillery.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/distilleries/{distillery.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_distillery_returns_404(self):
        """
        Verify that delete for a distillery that doesn't exist returns 404
        """
        response = self.client.delete(f"/distilleries/12345")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_distillery(self):
        """
        Ensures we get an existing distillery
        """
        distillery = Distillery()
        distillery.name = "Corsair"
        distillery.location = "some place"
        distillery.description = "it makes bourbon"
        distillery.link_to_site = "www.somewhere.com"
        distillery.distillery_img = "image.com"
        distillery.staff_member_id = 1
        distillery.save()

        response = self.client.get(f"/distilleries/{distillery.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "Corsair")
        self.assertEqual(json_response["location"], "some place")
        self.assertEqual(json_response["description"], "it makes bourbon")
        self.assertEqual(json_response["link_to_site"], "www.somewhere.com")
        self.assertEqual(json_response["distillery_img"], "image.com")
    
    def test_change_distillery(self):
        """
        Ensure we can change an existing distillery
        """
        distillery = Distillery()
        distillery.name = "Corsair"
        distillery.location = "some place"
        distillery.description = "it makes bourbon"
        distillery.distillery_img = "image.com"
        distillery.type_of_distillery_id = 1
        distillery.staff_member_id = 1
        distillery.save()

        data = {
            "name": "A Different Distillery",
            "location": "more stuff",
            "description": "stir it up",
            "link_to_site": "www.anotherwebsite.com",
            "distillery_img": "anotherimage.com"
        }

        response = self.client.put(f"/distilleries/{distillery.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/distilleries/{distillery.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["name"], "A Different Distillery")
        self.assertEqual(json_response["location"], "more stuff")
        self.assertEqual(json_response["description"], "stir it up")
        self.assertEqual(json_response["link_to_site"], "www.anotherwebsite.com")
        self.assertEqual(json_response["distillery_img"], "anotherimage.com")