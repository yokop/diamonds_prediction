from .models import MyLog


def add_log(logtype,message):
    new_log = MyLog.objects.create(logtype  = logtype,message = message)