import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import CustomUser as User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["password"]


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType, required=True)

    @staticmethod
    def resolve_users(root, info, **kwargs):
        """
        Resolves all users
        """

        return User.objects.all()
