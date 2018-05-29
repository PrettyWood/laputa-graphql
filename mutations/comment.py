import graphene

import models
from database import db_session
from schema import SmallApp, User, Comment


class CreateComment(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)
        slide_id = graphene.Int(required=True)
        message = graphene.String(required=True)

    comment = graphene.Field(lambda: Comment)
    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id, **kwargs):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"

        new_comment = models.Comment(user=user, small_app=small_app, **kwargs)
        db_session.add(new_comment)
        db_session.commit()
        return CreateComment(comment=new_comment, ok=True)


class UpdateComment(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)
        slide_id = graphene.Int(required=True)
        message = graphene.String(required=True)

    comment = graphene.Field(lambda: Comment)
    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id, slide_id, message):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"
        existing_comment = (Comment.get_query(info)
                                   .filter(models.Comment.user_id == user.id)
                                   .filter(models.Comment.small_app_id == small_app_id)
                                   .filter(models.Comment.slide_id == slide_id)
                                   .first())
        assert existing_comment is not None, f'No comment found for slide_id: {slide_id}'

        existing_comment.message = message
        db_session.add(existing_comment)
        db_session.commit()
        return UpdateComment(comment=existing_comment, ok=True)


class DeleteComment(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        small_app_id = graphene.String(required=True)
        slide_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, username, small_app_id, slide_id):
        user = User.get_query(info).filter(models.User.name == username).first()
        assert user is not None, f"User '{username}' does not exist"
        small_app = SmallApp.get_query(info).filter(models.SmallApp.id == small_app_id).first()
        assert small_app is not None, f"Small app '{small_app_id}' does not exist"
        existing_comment = (Comment.get_query(info)
                                   .filter(models.Comment.user_id == user.id)
                                   .filter(models.Comment.small_app_id == small_app_id)
                                   .filter(models.Comment.slide_id == slide_id)
                                   .first())
        assert existing_comment is not None, f'No comment found for slide_id: {slide_id}'

        db_session.delete(existing_comment)
        db_session.commit()
        return DeleteComment(ok=True)
