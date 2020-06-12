import graphene
import graphql_jwt
from django.core.exceptions import ValidationError
from graphene_django.types import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.models import get_user_model
from graphql_auth import mutations
from graphql_jwt.decorators import login_required


# Fix PasswordChange function
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    update_account = mutations.UpdateAccount.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    # password_change = mutations.PasswordChange.Field()
    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class PasswordChangeMutation(graphene.Mutation):
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
            return PasswordChangeMutation(user=user)
        except ValidationError as e:
            return PasswordChangeMutation(user=user, errors=e)


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, PasswordChangeMutation, graphene.ObjectType,):
    password_change = PasswordChangeMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
