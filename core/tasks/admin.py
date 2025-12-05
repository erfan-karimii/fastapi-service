from sqladmin import ModelView
from fastapi import Request
from .models import TaskModel


class IsVerifiedFilter:
    title = "Is Verified"
    parameter_name = "is_verified"

    def lookups(self, request, model) -> list[tuple[str, str]]:
        """
        Returns a list of tuples with the filter key and the human-readable label.
        """
        return [
            ("all", "All"),
            ("true", "Yes"),
            ("false", "No"),
        ]

    def get_filtered_query(self, query, value, model):
        """
        Returns a filtered query based on the filter value.
        """
        if value == "true":
            return query.filter(model.is_verified == True)
        elif value == "false":
            return query.filter(model.is_verified == False)
        else:
            return query


class TaskAdmin(ModelView, model=TaskModel):
    name = "Task"
    name_plural = "Tasks"
    edit_template = "custom_edit.html"
    column_list = [
        TaskModel.id,
        TaskModel.user_id,
        TaskModel.title,
        TaskModel.description,
        TaskModel.is_completed,
        TaskModel.created_date,
        TaskModel.updated_date,
    ]
    form_excluded_columns = [
        TaskModel.created_date,
        TaskModel.updated_date,
        TaskModel.deleted_at,
    ]
    icon = "fa-solid fa-check"
    can_export = True
    page_size = 10
    page_size_options = [1, 10, 25, 50, 100]

    def is_accessible(self, request: Request) -> bool:
        return True

    def is_visible(self, request: Request) -> bool:
        return True
