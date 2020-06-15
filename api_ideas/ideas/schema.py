import graphene
from django.core.exceptions import ObjectDoesNotExist
from following.models import Following
from graphene_django.types import DjangoObjectType
from graphene_subscriptions.events import CREATED
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from ideas.models import Idea


class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea


# Queries
class Query(object):
    get_ideas = graphene.List(IdeaType)
    get_user_ideas = graphene.List(IdeaType, user_id=graphene.Int(required=True),)
    get_timeline = graphene.List(IdeaType, first=graphene.Int(), skip=graphene.Int(),)

    # Resolving Ideas
    @login_required
    def resolve_get_ideas(self, info, **kwargs):
        return Idea.objects.filter(user=info.context.user.id).order_by("-created")

    @login_required
    def resolve_get_user_ideas(self, info, user_id):
        if user_id == info.context.user.id:
            return Idea.objects.filter(user=info.context.user.id).order_by("-created")
        else:
            get_ideas = Idea.objects.filter(user=user_id, status=Idea.PUBLIC)
            i_am_follower = Following.objects.filter(
                follower=info.context.user.id,
                followed=user_id,
                status=Following.APPROVED,
            )
            if i_am_follower:
                get_protected_ideas = Idea.objects.filter(
                    user=user_id, status=Idea.PROTECTED
                )
                return get_ideas.union(get_protected_ideas).order_by("-created")
            return get_ideas.order_by("-created")

    # Resolving special Feature: Timeline
    @login_required
    def resolve_get_timeline(self, info):
        accesible_notes = [Idea.PUBLIC, Idea.PROTECTED]
        my_ideas = Idea.objects.filter(user=info.context.user.id)
        following_list = Following.objects.filter(
            follower=info.context.user.id, status=Following.APPROVED
        ).values_list("followed", flat=True)
        following_ideas = Idea.objects.filter(
            user__in=following_list, status__in=accesible_notes
        )
        if following_ideas:
            return my_ideas.union(following_ideas).order_by("-created")
        return my_ideas.order_by("-created")


def check_exists(info, id):
    try:
        idea = Idea.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise GraphQLError("The idea not exists!")
    if idea.user_id != info.context.user.id:
        raise GraphQLError("You are not the owner!")
    return idea


# Mutations
class CreateIdea(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        idea = graphene.String(required=True)
        status = graphene.Int(required=False)

    @login_required
    def mutate(self, info, idea, **kwargs):
        # Optional field: default PUBLIC
        status = kwargs.get("status", Idea.PUBLIC)
        idea = Idea(idea=idea, status=status, user_id=info.context.user.id)
        idea.save()
        return CreateIdea(idea=idea)


class RemoveIdea(graphene.Mutation):
    id = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        idea = check_exists(info, id)
        idea.delete()
        return RemoveIdea(id=id)


class SetStatusIdea(graphene.Mutation):
    idea = graphene.Field(IdeaType)

    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id, status):
        idea = check_exists(info, id)
        idea.status = status
        idea.save()
        return SetStatusIdea(idea=idea)


class Mutation(graphene.ObjectType):
    create_idea = CreateIdea.Field()
    remove_idea = RemoveIdea.Field()
    status_idea = SetStatusIdea.Field()


class Subscription(graphene.ObjectType):
    idea_created = graphene.Field(IdeaType)

    def resolve_idea_created(root, info):

        following_user_ids = Following.objects.filter(
            follower=info.context.user, status=Following.APPROVED
        ).values_list("followed__id", flat=True)

        return root.filter(
            lambda event: event.operation == CREATED
            and isinstance(event.instance, Idea)
            and event.instance.user.pk in following_user_ids
            and event.instance.status in [Idea.PUBLIC, Idea.PROTECTED]
        ).map(lambda event: event.instance)
