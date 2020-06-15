import graphene
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
from following.models import Following
from users.models import CustomUser


class FollowingType(DjangoObjectType):
    class Meta:
        model = Following


class Query(object):
    get_follow_requests = graphene.List(
        FollowingType,
    )
    get_followers = graphene.List(
        FollowingType,
    )
    get_following = graphene.List(
        FollowingType,
    )

    @login_required
    def resolve_get_follow_requests(self, info):
        return Following.objects.filter(
            followed=info.context.user.id).filter(
            status=Following.PENDING
        )

    @login_required
    def resolve_get_followers(self, info, **kwargs):
        return Following.objects.filter(
            followed=info.context.user.id).filter(
            status=Following.APPROVED
        )

    @login_required
    def resolve_get_following(self, info, **kwargs):
        return Following.objects.filter(
            follower=info.context.user.id).filter(
            status=Following.APPROVED
        )


# Mutate Following
class FollowRequest(graphene.Mutation):
    current_request = graphene.Field(FollowingType)

    class Arguments:
        user_to_follow = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_to_follow):
        try:
            user_followed = CustomUser.objects.get(pk=user_to_follow)
        except ObjectDoesNotExist:
            raise GraphQLError('The user to follow not exists!')
        do_follow_request = Following(
            follower=info.context.user,
            followed=user_followed,
            status=Following.PENDING,
        )
        do_follow_request.save()
        return FollowRequest(current_request=do_follow_request)


class UnfollowUser(graphene.Mutation):
    current_request = graphene.Field(FollowingType)

    class Arguments:
        user_to_unfollow = graphene.Int(required=True)

    @login_required
    def mutate(self, info, user_to_unfollow):
        try:
            unfollow_request = Following.objects.filter(
                follower=info.context.user
            ).get(followed=user_to_unfollow)
        except ObjectDoesNotExist:
            raise GraphQLError('The user not exists or not following!')
        unfollow_request.delete()
        return UnfollowUser(current_request=unfollow_request)


class RemoveFollower(graphene.Mutation):
    current_request = graphene.Field(FollowingType)

    class Arguments:
        follower_to_remove = graphene.Int(required=True)

    @login_required
    def mutate(self, info, follower_to_remove):
        try:
            remove_follower = Following.objects.filter(
                followed=info.context.user
            ).get(follower=follower_to_remove)
        except ObjectDoesNotExist:
            raise GraphQLError('The user is not following you or not exists!')
        remove_follower.delete()
        return RemoveFollower(current_request=remove_follower)


def get_exact_follower(info, id):
    try:
        return Following.objects.filter(
            followed=info.context.user.id
        ).get(
            follower=id
        )
    except ObjectDoesNotExist:
        raise GraphQLError('The follow request does not exists!')


class AproveFollower(graphene.Mutation):
    current_request = graphene.Field(FollowingType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        followers = get_exact_follower(info, id)
        followers.status = Following.APPROVED
        followers.save()
        return AproveFollower(current_request=followers)


class DenyFollower(graphene.Mutation):
    current_request = graphene.Field(FollowingType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        followers = get_exact_follower(info, id)
        followers.status = Following.DENIED
        followers.save()
        return DenyFollower(current_request=followers)


class Mutation(graphene.ObjectType):
    do_follow_request = FollowRequest.Field()
    unfollow_user = UnfollowUser.Field()
    remove_follower = RemoveFollower.Field()
    aprove_follower = AproveFollower.Field()
    deny_follower = DenyFollower.Field()
