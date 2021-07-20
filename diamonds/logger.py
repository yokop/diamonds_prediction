from .models import MyLog

# enables logging. the log is shown on admin page
def add_log(logtype,message):
    new_log = MyLog.objects.create(logtype  = logtype,message = message)