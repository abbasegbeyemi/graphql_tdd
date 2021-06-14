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


class UserCreateMutationInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String()


class UserCreate(graphene.Mutation):
    """
    Mutation to create a user.
    Attributes for the class to determine the mutation response
    """

    id = graphene.ID()

    class Arguments:
        """
        Input argumants for creating the user
        """
        user_data = UserCreateMutationInput(required=True)

    @staticmethod
    def mutate(root, info, user_data=None):
        """
        Create the user and return specified attribtes
        """
        user = User.objects.create_user(**user_data)

        return UserCreate(id=user.id)


class UserMutation(graphene.ObjectType):
    """
    Mutation for users
    """
    user_create = UserCreate.Field()
