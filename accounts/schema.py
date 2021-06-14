import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import CustomUser as User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["password"]


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, required=True, user_id=graphene.Int(required=True))
    users = graphene.List(UserType, required=True)

    @staticmethod
    def resolve_users(root, info, **kwargs):
        """
        Resolves all users
        """

        return User.objects.all()

    @staticmethod
    def resolve_user(root, info, user_id, **kwargs):
        """
        Resolves a single user
        """
        return User.objects.get_by_id(user_id)
