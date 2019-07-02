from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'myroductivitytool.common'
    verbose_name = 'common'

    def ready(self):
        import myroductivitytool.common.signals
