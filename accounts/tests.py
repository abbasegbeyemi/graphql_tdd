import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from graphene_django.utils import GraphQLTestCase


class UserManagerTests(TestCase):
    """
    Set the user model
    """
    User = get_user_model()

    def test_create_user(self):
        """
        Tests creating a standard user.
        Test that the user is created with the set variables.
        Test if there is a tpe error if no params are passed in.
        Test if there is a type error if no password is passed in.
        Test if there is a value error is email is blank.
        Test if there is a value error while trying to create a sueruser with normal
        user method.
        """

        email = "samson@kwale.com"
        password = "strong22"
        first_name = "Samson"
        last_name = "Kwame"
        occupation = "Accountant"
        company = "Kwale Tech"

        user = self.User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            occupation=occupation,
            company=company,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.occupation, occupation)
        self.assertEqual(user.company, company)

        with self.assertRaises(TypeError):
            self.User.objects.create_user()

        with self.assertRaises(TypeError):
            self.User.objects.create_user(email="")

        with self.assertRaises(ValueError):
            self.User.objects.create_user(email="", password=password)

        with self.assertRaises(ValueError):
            self.User.objects.create_user(email=email, password=password, is_superuser=True)

    def test_create_superuser(self):
        """
        Tests creating a superuser
        Test that the superuser is created with set variables.
        Test if there is a value error trying to create a normal user with the superuser method
        """
        email = "kida@kudz.ng"
        password = "turnup22"
        first_name = "Kida"
        last_name = "Kudz"
        occupation = "Designer"
        company = "Kudz Company"

        user = self.User.objects.create_superuser(
            email=email,
            first_name=first_name,
            password=password,
            last_name=last_name,
            company=company,
            occupation=occupation
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.occupation, occupation)
        self.assertEqual(user.company, company)
        self.assertTrue(user.is_superuser)

        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                email="failfast@fail.com",
                password="notstrongatall",
                is_superuser=False
            )

    def test_get_by_id(self):
        """
        Tests user get by id
        Tests if method has valie
        Tests if user exists
        """

        email = "kida@kudz.ng"
        password = "turnup22"
        first_name = "Kida"
        last_name = "Kudz"
        occupation = "Designer"
        company = "Kudz Company"

        user = self.User.objects.create_superuser(
            email=email,
            first_name=first_name,
            password=password,
            last_name=last_name,
            company=company,
            occupation=occupation
        )

        user = self.User.objects.get_by_id(user.id)

        self.assertTrue(user.is_superuser)
        self.assertEqual(user.occupation, occupation)
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.company, company)

        with self.assertRaises(ValueError):
            self.User.objects.get_by_id()

        with self.assertRaises(self.User.DoesNotExist):
            self.User.objects.get_by_id(99)


class TestUserApiCalls(GraphQLTestCase):
    User = get_user_model()

    def test_user_query(self):
        """
        Test that a user created in the database is returned in a graphql query
        """
        new_user = self.User.objects.create_user(
            email="ae@email.com",
            password="strong2323",
            first_name="Abbas"
        )
        response = self.query(
            '''
            query {
                users {
                    id
                    firstName
                    email
                }
            }
            ''',
        )

        content = json.loads(response.content)

        # Validate that no errors were received
        self.assertResponseNoErrors(response)

        user_data = content["data"]["users"][0]

        self.assertEqual(user_data["id"], str(new_user.id))
        self.assertEqual(user_data["firstName"], new_user.first_name)
        self.assertEqual(user_data["email"], new_user.email)
