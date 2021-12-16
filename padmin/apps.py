from django.apps import AppConfig


class AdminConfig(AppConfig):
    name = 'padmin'


    def ready(self):
        from padmin import scheduler
        # scheduler.happybirthday()
        # scheduler.greet()
        # scheduler.customsheduled()