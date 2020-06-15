import pytest
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from graphene.test import Client
from mixer.backend.django import mixer
from ideas.models import Idea
from users.models import CustomUser
from api_ideas.schema import schema


class IdeaType(DjangoObjectType):
    class Meta:
        model = Idea


GET_IDEAS = """
    query {
        getIdeas {
            id
            idea
            status
            created
            user {
                id
                username
            }
        }
    }
"""

TEXT_IDEA = "This is a sample text"
STATUS_IDEA_CHOICE = "A_2"
STATUS_IDEA_CHOICE_DEFAULT = "A_1"

CREATE_IDEA = """
    mutation {
        createIdea(idea: "This is a sample text", status:2) {
            idea {
                id
                idea
                status
                created
            }
        }
    }
"""

CREATE_IDEA_NO_STATUS = """
    mutation {
        createIdea(idea: "This is a sample text") {
            idea {
                id
                idea
                status
                created
            }
        }
    }
"""


@pytest.mark.django_db
class TestIdeaSchema(TestCase):
    def setUp(self):
        request_factory = RequestFactory()
        self.client = Client(schema)
        self.my_request = request_factory.get("/api/")
        self.user = mixer.blend(CustomUser)
        self.my_request.user = self.user

    def test_get_ideas(self):
        mixer.blend(Idea, user=self.user)
        mixer.blend(Idea, user=self.user)
        response = self.client.execute(GET_IDEAS, context_value=self.my_request)
        ideas = response.get("data").get("getIdeas")
        assert len(ideas) > 1

    def test_create_idea(self):
        response = self.client.execute(CREATE_IDEA,context_value=self.my_request)
        response_idea = response.get("data").get("createIdea").get("idea")
        idea = response_idea.get("idea")
        status = response_idea.get("status")
        assert idea == TEXT_IDEA
        assert status == STATUS_IDEA_CHOICE

    def test_create_idea_no_status(self):
        response = self.client.execute(CREATE_IDEA_NO_STATUS,context_value=self.my_request)
        response_idea = response.get("data").get("createIdea").get("idea")
        idea = response_idea.get("idea")
        status = response_idea.get("status")
        assert idea == TEXT_IDEA
        assert status == STATUS_IDEA_CHOICE_DEFAULT

    def test_str_model_idea(self):
        idea = Idea()
        idea.idea = TEXT_IDEA
        idea.status = STATUS_IDEA_CHOICE_DEFAULT
        assert idea.__str__() == f"{TEXT_IDEA} ({STATUS_IDEA_CHOICE_DEFAULT})"

