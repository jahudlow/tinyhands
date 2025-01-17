from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from accounts.tests.factories import Address2UserFactory, BadAddress2UserFactory
from dataentry.models import Address2
from dataentry.models import Person
from dataentry.models import VictimInterview
from dataentry.models import VictimInterviewLocationBox
from dataentry.tests.factories import Address2Factory, Address1Factory, CanonicalNameFactory, PersonFactory, VifFactory


class Address1Test(APITestCase):
    def setUp(self):
        self.address1_list = Address1Factory.create_batch(20)
        self.user = Address2UserFactory.create()
        self.client.force_authenticate(user=self.user)
        self.data = {
            'name': 'Address1',
            "completed": False,
        }

    def test_create_address1_complete_data(self):
        url = reverse('Address1')

        self.data["level"] = "City"
        self.data["latitude"] = 27.713855
        self.data["longitude"] = 85.314800


        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Address1')
        self.assertEqual(response.data['level'], 'City')
        self.assertEqual(response.data['latitude'], 27.713855)
        self.assertEqual(response.data['longitude'], 85.314800)
        self.assertEqual(response.data['completed'], False)
        self.assertIsNotNone(response.data['id'])

    def test_create_address1_incomplete_data(self):
        # Should be able to save address1 with null level, latitude, and longitude
        url = reverse('Address1')

        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Address1')
        self.assertEqual(response.data['level'], 'District')
        self.assertEqual(response.data['latitude'], 0)
        self.assertEqual(response.data['latitude'], 0)
        self.assertEqual(response.data['completed'], False)
        self.assertIsNotNone(response.data['id'])

    def test_list_address1s(self):
        url = reverse('Address1')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 20)  # 20 is coming from the 20 Address2s we made which each have their own Address1

    def test_list_all_address1s(self):
        """
            This one doesn't paginate the addresses
        """
        url = reverse('Address1all')

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 20)  # 20 is coming from the 20 Address2s we made which each have their own Address1

    def test_retrieve_address1(self):
        url = reverse('Address1detail', args=[self.address1_list[0].id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.address1_list[0].id)  # 1 is the arg we passed into the url

    def test_update_address1(self):
        url = reverse('Address1detail', args=[self.address1_list[0].id])
        data = {'name': "updatedAddress1"}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.address1_list[0].id)  # 1 is the arg we passed into the url
        self.assertEqual(response.data['name'], "updatedAddress1")  # 1 is the arg we passed into the url

    def test_remove_address1(self):
        address1 = Address1Factory.create()
        url = reverse('Address1detail', args=[address1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the address doesn't exist anymore
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_address1_403_if_doesnt_have_permission(self):
        self.bad_user = BadAddress2UserFactory.create()
        self.client.force_authenticate(user=self.bad_user)

        address2 = CanonicalNameFactory.create()

        # get detail
        url = reverse('Address1detail', args=[address2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # put detail
        url = reverse('Address1detail', args=[address2.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete detail
        url = reverse('Address1detail', args=[address2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Address1RelatedItems', args=[address2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        # get
        url = reverse('Address1')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # post
        url = reverse('Address1')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Address2Test(APITestCase):

    def setUp(self):
        self.user = Address2UserFactory.create()
        self.client.force_authenticate(user=self.user)

        self.Address2List = Address2Factory.create_batch(20)
        self.factory = APIRequestFactory()
        self.first_address1 = self.Address2List[0].address1
        self.first_canonical_name = self.Address2List[0].canonical_name
        self.data = {
            'name': 'Address2',
            "verified": False,
            "address1": {
                "id": self.first_address1.id,
                "name": self.first_address1.name,
            },
            "canonical_name": {
                "id": self.first_canonical_name.id,
                "name": self.first_canonical_name.name,
            },
        }

    def test_create_address2(self):
        self.data["latitude"] = 29.1837169619
        self.data["longitude"] = 81.2336041444
        self.data["level"] = "City"

        url = reverse('Address2')

        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data['name'], 'Address2')
        self.assertEqual(response.data['level'], "City")
        self.assertEqual(response.data["latitude"], 29.1837169619)
        self.assertEqual(response.data["longitude"],  81.2336041444)
        self.assertEqual(response.data['address1']['id'], self.first_address1.id)
        self.assertEqual(response.data['canonical_name']['id'], self.first_canonical_name.id)

    def test_create_address2_incomplete_data(self):
        url = reverse('Address2')
        self.data["canonical_name"] = {"id": -1, "name": "Null"}
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data["level"], "VDC")
        self.assertEqual(response.data["latitude"], 0)
        self.assertEqual(response.data["longitude"],0)
        self.assertEqual(response.data['name'], 'Address2')
        self.assertEqual(response.data['address1']['id'], self.first_address1.id)
        self.assertEqual(response.data['canonical_name'], None)

    def test_update_address2(self):
        address2 = Address2Factory.create()
        url = reverse('Address2detail', args=[address2.id])

        self.data['id'] = address2.id
        self.data['name'] = "Address2Updated"
        self.data["level"] = "District"
        self.data["latitude"] = 29.1337
        self.data["longitude"]= 81.188118

        response = self.client.put(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Address2Updated')
        self.assertEqual(response.data['id'], address2.id)
        self.assertEqual(response.data["level"], "District")
        self.assertEqual(response.data["latitude"], 29.1337)
        self.assertEqual(response.data["longitude"],81.188118)

    def test_update_address2_canonical_name_null(self):
        # Should be able to save address2 with null canonical name
        address2 = Address2Factory.create()
        url = reverse('Address2detail', args=[address2.id])

        self.data['id'] = address2.id
        self.data['name'] = "Address2Updated"
        self.data["canonical_name"] = {"id": -1, "name": "Null"}

        response = self.client.put(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['id'])
        self.assertEqual(response.data['name'], 'Address2Updated')
        self.assertEqual(response.data['address1']['id'], self.first_address1.id)
        self.assertEqual(response.data['canonical_name'], None)

    def test_remove_address2(self):
        address2 = Address2Factory.create()
        url = reverse('Address2detail', args=[address2.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the address doesn't exist anymore
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_address2(self):
        address2 = Address2Factory.create()
        url = reverse('Address2detail', args=[address2.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], address2.id)
        self.assertEqual(response.data['name'], address2.name)

    def test_retrieve_address2_canonical_name_null(self):
        address2 = CanonicalNameFactory.create()
        url = reverse('Address2detail', args=[address2.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], address2.id)
        self.assertEqual(response.data['name'], address2.name)
        self.assertEqual(response.data['canonical_name'], None)

    def test_403_if_doesnt_have_permission(self):
        self.bad_user = BadAddress2UserFactory.create()
        self.client.force_authenticate(user=self.bad_user)

        address2 = CanonicalNameFactory.create()

        # get detail
        url = reverse('Address2detail', args=[address2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # put detail
        url = reverse('Address2detail', args=[address2.id])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # delete detail
        url = reverse('Address2detail', args=[address2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        url = reverse('Address2RelatedItems', args=[address2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # get
        url = reverse('Address2')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # post
        url = reverse('Address2')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
