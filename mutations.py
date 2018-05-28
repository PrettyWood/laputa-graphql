from datetime import datetime

import graphene

import models
from database import db_session
from schema import SmallApp


class CreateSmallApp(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=True)

    small_app = graphene.Field(lambda: SmallApp)
    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        small_app = models.SmallApp(**kwargs)
        db_session.add(small_app)
        db_session.commit()
        return CreateSmallApp(small_app=small_app, ok=True)


class UpdateSmallApp(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String()
        stage = graphene.Enum.from_enum(models.Stage)()

    # Class attributes
    small_app = graphene.Field(lambda: SmallApp)
    ok = graphene.Boolean()

    def mutate(self, info, id, name=None, stage=None):
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == id).first()
        if name:
            small_app.name = name
        if stage == models.Stage.STAGING.value:
            small_app.staging_last_update = datetime.now()
        elif stage == models.Stage.PRODUCTION.value:
            small_app.production_last_update = datetime.now()
        db_session.add(small_app)
        db_session.commit()
        return UpdateSmallApp(small_app=small_app, ok=True)


class DeleteSmallApp(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == id).first()
        db_session.delete(small_app)
        db_session.commit()
        return DeleteSmallApp(ok=True)
