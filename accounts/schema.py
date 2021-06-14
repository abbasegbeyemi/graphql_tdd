import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import CustomUser as User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ["password"]


class UserQuery(graphene.ObjectType):
    me = graphene.Field(UserType, required=True)
    user = graphene.Field(UserType, required=True, user_id=graphene.Int(required=True))
    users = graphene.List(UserType, required=True)

    @staticmethod
    @login_required
    def resolve_me(root, info, **kwargs):
        """
        Resolves a logged in user
        """
        return info.context.user

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
    """
    Input values for user creation mutation
    """
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String()


class UserCreate(graphene.Mutation):
    """
    Mutation to create a user.
    Returns the id of the created user.
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
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
