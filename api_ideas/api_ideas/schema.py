import following.schema
import graphene
import graphql_jwt
import ideas.schema
import users.schema
from graphene_django.types import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import MeQuery, UserQuery
from graphql_jwt.decorators import login_required


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(
    UserQuery, MeQuery,
    users.schema.Query,
    ideas.schema.Query,
    following.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    AuthMutation,
    users.schema.Mutation,
    ideas.schema.Mutation,
    following.schema.Mutation,
    graphene.ObjectType,
):
    pass


class Subscription(
    ideas.schema.Subscription
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
