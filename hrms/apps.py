from django.apps import AppConfig

class HrmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrms'


class LeaveRequestConfig(AppConfig):
    name = 'leave_request'

    def ready(self):
        import hrms.signals  
