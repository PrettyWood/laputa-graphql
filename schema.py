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


class Privilege(SQLAlchemyObjectType):
    class Meta:
        model = models.Privilege


class Query(graphene.ObjectType):
    # SMALL APPS
    small_app = graphene.Field(SmallApp,
                               id=graphene.String(required=False),
                               name=graphene.String(required=False))
    all_small_apps = graphene.List(SmallApp)

    def resolve_small_app(self, info, **kwargs):
        query = SmallApp.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.SmallApp, key) == value)
        return query.first()

    def resolve_all_small_apps(self, info):
        return SmallApp.get_query(info).all()

    # USERS
    user = graphene.Field(User,
                          name=graphene.String(required=True))
    all_users = graphene.List(User)

    def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.User, key) == value)
        return query.first()

    def resolve_all_users(self, info):
        return User.get_query(info).all()

    # GROUPS
    group = graphene.Field(Group,
                           name=graphene.String(required=True))
    all_groups = graphene.List(Group)

    def resolve_group(self, info, **kwargs):
        query = Group.get_query(info)
        for key, value in kwargs.items():
            query = query.filter(getattr(models.Group, key) == value)
        return query.first()

    def resolve_all_groups(self, info):
        return Group.get_query(info).all()

    # PRIVILEGES
    privilege = graphene.Field(Privilege,
                               username=graphene.String(required=True),
                               small_app_id=graphene.String(required=True))
    privileges = graphene.List(Privilege,
                               username=graphene.String(required=True))
    all_privileges = graphene.List(Privilege)

    def resolve_privilege(self, info, username, small_app_id):
        user = (User.get_query(info)
                    .filter(models.User.name == username)
                    .first())
        return (Privilege.get_query(info)
                         .filter(models.Privilege.user_id == user.id)
                         .filter(models.Privilege.small_app_id == small_app_id)
                         .first())

    def resolve_privileges(self, info, username):
        user = (User.get_query(info)
                    .filter(models.User.name == username)
                    .first())
        return (Privilege.get_query(info)
                         .filter(models.Privilege.user_id == user.id)
                         .all())

    def resolve_all_privileges(self, info):
        return Privilege.get_query(info).all()


from mutations.small_app import CreateSmallApp, UpdateSmallApp, DeleteSmallApp
from mutations.user import CreateUser, UpdateUser, DeleteUser
from mutations.group import CreateGroup, UpdateGroup, DeleteGroup
from mutations.privilege import CreatePrivilege, UpdatePrivilege, DeletePrivilege


class Mutation(graphene.ObjectType):
    createSmallApp = CreateSmallApp.Field()
    updateSmallApp = UpdateSmallApp.Field()
    deleteSmallApp = DeleteSmallApp.Field()

    createUser = CreateUser.Field()
    updateUser = UpdateUser.Field()
    deleteUser = DeleteUser.Field()

    createGroup = CreateGroup.Field()
    updateGroup = UpdateGroup.Field()
    deleteGroup = DeleteGroup.Field()

    createPrivilege = CreatePrivilege.Field()
    updatePrivilege = UpdatePrivilege.Field()
    deletePrivilege = DeletePrivilege.Field()


schema = graphene.Schema(query=Query, mutation=Mutation,
                         types=[SmallApp, User, Group, Privilege])
