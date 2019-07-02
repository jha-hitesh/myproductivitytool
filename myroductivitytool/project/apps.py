from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'myroductivitytool.project'
    verbose_name = 'project'

    def ready(self):
        import myroductivitytool.project.signals
