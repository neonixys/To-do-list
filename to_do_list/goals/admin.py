from django.contrib import admin

from to_do_list.goals.models import GoalCategory


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
    list_filter = ("is_deleted",)


admin.site.register(GoalCategory, GoalCategoryAdmin)
