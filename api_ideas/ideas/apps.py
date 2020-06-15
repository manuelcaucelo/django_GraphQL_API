from django.apps import AppConfig


class IdeaConfig(AppConfig):
    name = "ideas"

    def ready(self):
        import ideas.signals
