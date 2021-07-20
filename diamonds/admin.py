from django.contrib import admin
from .models import Diamond
from .models import Diamond_predicted
from .models import MyLog

class Diamond_predicted_admin(admin.ModelAdmin):
    read_only_fields = ('created',)

# Register your models here.
admin.site.register(Diamond)
admin.site.register(Diamond_predicted,Diamond_predicted_admin)
admin.site.register(MyLog)
