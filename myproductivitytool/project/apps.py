from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'myproductivitytool.project'
    verbose_name = 'project'

    def ready(self):
        import myproductivitytool.project.signals
