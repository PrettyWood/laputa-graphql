import graphene
import models
from graphene_sqlalchemy import SQLAlchemyObjectType


class SmallApp(SQLAlchemyObjectType):
    class Meta:
        model = models.SmallApp


class User(SQLAlchemyObjectType):
    class Meta:
        model = models.User


class Group(SQLAlchemyObjectType):
    class Meta:
        model = models.Group


class Query(graphene.ObjectType):
    # SMALL APPS
    small_app = graphene.Field(SmallApp,
                               id=graphene.String(required=False),
                               name=graphene.String(required=False))
    small_apps = graphene.List(SmallApp)

    def resolve_small_app(self, info, **kwargs):
        query = SmallApp.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.SmallApp, key) == value)
        return query.first()

    def resolve_small_apps(self, info):
        query = SmallApp.get_query(info)
        return query.all()

    # USERS
    user = graphene.Field(User,
                          name=graphene.String(required=True))
    users = graphene.List(User)

    def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.User, key) == value)
        return query.first()

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    # GROUPS
    group = graphene.Field(Group,
                           name=graphene.String(required=True))
    groups = graphene.List(Group)

    def resolve_group(self, info, **kwargs):
        query = Group.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.Group, key) == value)
        return query.first()

    def resolve_groups(self, info):
        query = Group.get_query(info)
        return query.all()

from mutations import CreateSmallApp, UpdateSmallApp, DeleteSmallApp


class Mutation(graphene.ObjectType):
    createSmallApp = CreateSmallApp.Field()
    updateSmallApp = UpdateSmallApp.Field()
    deleteSmallApp = DeleteSmallApp.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[SmallApp])
