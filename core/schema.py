import graphene

from accounts.schema import UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
