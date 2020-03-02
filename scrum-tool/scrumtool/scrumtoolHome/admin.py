from django.contrib import admin
from .models import ProductBacklog, SprintBacklog, TaskCard, adminUser, normalUser


admin.site.register(ProductBacklog)
admin.site.register(SprintBacklog)
admin.site.register(TaskCard)
admin.site.register(adminUser)
admin.site.register(normalUser)


