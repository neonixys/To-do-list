from django.db import models

from to_do_list.core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    class Meta:
        abstract = True


class GoalCategory(BaseModel):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, "To Do"
        in_progress = 2, "In Progress"
        done = 3, "Done"
        archived = 4, "Archived"

    class Priority(models.IntegerChoices):
        low = 1, "Low"
        medium = 2, "Medium"
        high = 3, "High"
        critical = 4, "Critical"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name="goals")
    due_date = models.DateTimeField(verbose_name="Дата окончания", null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goals")
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.medium)

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self):
        return self.title


class GoalComment(BaseModel):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goal_comments")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, related_name="goal_comments")
    text = models.TextField(verbose_name="Текст комментария")
