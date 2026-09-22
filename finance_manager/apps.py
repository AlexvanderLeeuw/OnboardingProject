from django.apps import AppConfig


class FinanceManagerConfig(AppConfig):
    name = 'finance_manager'

    def ready(self):
        import finance_manager.signals
