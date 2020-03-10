from django.contrib import admin
from .models import ProductBacklog, SprintBacklog, TaskCard, Checklist, ChecklistItem


admin.site.register(ProductBacklog)
admin.site.register(SprintBacklog)
admin.site.register(TaskCard)
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
