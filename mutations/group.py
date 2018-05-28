import graphene

import models
from database import db_session
from schema import Group


class CreateGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    group = graphene.Field(lambda: Group)
    ok = graphene.Boolean()

    def mutate(self, info, name):
        group = models.Group(name=name)
        db_session.add(group)
        db_session.commit()
        return CreateGroup(group=group, ok=True)


class UpdateGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        new_name = graphene.String(required=True)

    group = graphene.Field(lambda: Group)
    ok = graphene.Boolean()

    def mutate(self, info, name, new_name):
        group = Group.get_query(info).filter(models.Group.name == name).first()
        group.name = new_name
        db_session.add(group)
        db_session.commit()
        return UpdateGroup(group=group, ok=True)


class DeleteGroup(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, name):
        group = Group.get_query(info).filter(models.Group.name == name).first()
        db_session.delete(group)
        db_session.commit()
        return DeleteGroup(ok=True)
