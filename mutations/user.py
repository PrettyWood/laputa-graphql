import graphene

import models
from database import db_session
from schema import Group, User


Role = graphene.Enum.from_enum(models.Role)


class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        groups = graphene.List(graphene.String)
        role = Role()

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()

    def mutate(self, info, name, groups=None, role=None):
        _groups = []
        if groups is not None:
            existing_groups = [g.name for g in Group.get_query(info).all()]
            for g in groups:
                assert g in existing_groups, f'Group {g} does not exist. ' \
                                             f'Existing groups: {existing_groups}'
                _groups.append(Group.get_query(info).filter(models.Group.name == g).first())
        user = models.User(name=name, role=role, groups=_groups)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user, ok=True)


class UpdateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        groups = graphene.List(graphene.String)
        role = Role()

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()

    def mutate(self, info, name, groups=None, role=None):
        user = User.get_query(info).filter(models.User.name == name).first()
        _groups = []
        if groups is not None:
            existing_groups = [g.name for g in Group.get_query(info).all()]
            for g in groups:
                assert g in existing_groups, f'Group {g} does not exist. ' \
                                             f'Existing groups: {existing_groups}'
                _groups.append(Group.get_query(info).filter(models.Group.name == g).first())
        user.groups = _groups
        if role is not None:
            user.role = Role.get(role)
        db_session.add(user)
        db_session.commit()
        return UpdateUser(user=user, ok=True)


class DeleteUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, name):
        user = User.get_query(info).filter(models.User.name == name).first()
        db_session.delete(user)
        db_session.commit()
        return DeleteUser(ok=True)
