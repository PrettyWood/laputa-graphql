import graphene

import models
from database import db_session
from schema import SmallApp, User, Privilege

_PrivilegeEnum = graphene.Enum.from_enum(models.PrivilegeEnum)


class CreatePrivilege(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)
        privilege = _PrivilegeEnum(required=True)

    privilege = graphene.Field(lambda: Privilege)
    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id, privilege):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"
        privilege = models.PrivilegeEnum(privilege)

        new_privilege = models.Privilege(user=user, small_app=small_app, privilege=privilege)
        db_session.add(new_privilege)
        db_session.commit()
        return CreatePrivilege(privilege=new_privilege, ok=True)


class UpdatePrivilege(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)
        privilege = _PrivilegeEnum(required=True)

    privilege = graphene.Field(lambda: Privilege)
    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id, privilege):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"
        existing_privilege = (Privilege.get_query(info)
                                       .filter(models.SmallApp.id == small_app_id)
                                       .first())
        assert existing_privilege is not None, f'No privilege found'

        existing_privilege.privilege = models.PrivilegeEnum(privilege)
        db_session.add(existing_privilege)
        db_session.commit()
        return UpdatePrivilege(privilege=existing_privilege, ok=True)


class DeletePrivilege(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"
        existing_privilege = (Privilege.get_query(info)
                                       .filter(models.SmallApp.id == small_app_id)
                                       .first())
        db_session.delete(existing_privilege)
        db_session.commit()
        return DeletePrivilege(ok=True)
