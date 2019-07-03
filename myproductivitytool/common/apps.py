from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'myproductivitytool.common'
    verbose_name = 'common'

    def ready(self):
        import myproductivitytool.common.signals
