from django.apps import AppConfig


class PlanningPokerConfig(AppConfig):
    name = 'planning_poker'

# import signals
    def ready(self):
        import planning_poker.signals
        print('Hello')
