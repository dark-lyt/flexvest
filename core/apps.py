from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from taskManager import run_tasks
        run_tasks.start()
