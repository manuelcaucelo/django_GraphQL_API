import graphene
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from users.models import CustomUser


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser


class Query(object):
    find_username = graphene.List(
        UserType,
        username=graphene.String(required=True),
        first=graphene.Int(),
        skip=graphene.Int(),
    )

    @login_required
    def resolve_find_username(self, info, username, **kwargs):
        # Added simple optional pagination
        skip = kwargs.get("skip", None)
        first = kwargs.get("first", None)
        usernames = CustomUser.objects.filter(username__contains=username)
        if skip:
            usernames = usernames[skip:]
        if first:
            usernames = usernames[:first]
        return usernames


class ChangePassword(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)

    @login_required
    def mutate(self, info, password):
        user = info.context.user
        user.set_password(password)
        try:
            user.full_clean()
            user.save()
            return ChangePassword(user=user)
        except ValidationError as e:
            return ChangePassword(user=user, errors=e)


class Mutation(graphene.ObjectType):
    change_password = ChangePassword.Field()
