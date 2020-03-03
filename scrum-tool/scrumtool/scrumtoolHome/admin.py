from django.contrib import admin
from .models import ProductBacklog, SprintBacklog, TaskCard


admin.site.register(ProductBacklog)
admin.site.register(SprintBacklog)
admin.site.register(TaskCard)

