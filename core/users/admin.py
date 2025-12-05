from sqladmin import ModelView, action

from sqlalchemy import update
from fastapi import Request
from fastapi.responses import RedirectResponse
from .models import UserModel


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


class UserAdmin(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_export = True
    column_list = [
        UserModel.id,
        UserModel.email,
        UserModel.username,
        UserModel.is_active,
        UserModel.is_verified,
        UserModel.user_register_type,
    ]
    column_searchable_list = [UserModel.username, UserModel.email]
    column_sortable_list = [UserModel.id, UserModel.username, UserModel.email]
    column_details_exclude_list = [UserModel.password]
    form_excluded_columns = [
        UserModel.created_date,
        UserModel.updated_date,
        UserModel.deleted_at,
    ]
    column_labels = {UserModel.user_register_type: "Registration Type"}
    # column_filters = [IsVerifiedFilter]
    page_size = 10
    page_size_options = [1, 10, 25, 50, 100]

    def is_accessible(self, request: Request) -> bool:
        return True

    def is_visible(self, request: Request) -> bool:
        return True

    form_ajax_refs = {
        "tasks": {
            "fields": ("title",),
            "order_by": "id",
        }
    }

    @action(
        name="verify_users",
        label="Verify selected items",
        confirmation_message="Are you sure you want to verify the selected users?",
        add_in_detail=True,
        add_in_list=True,
    )
    async def verify_users(self, request: Request):
        pks = request.query_params.get("pks", "").split(",")
        if pks:
            with self.session_maker() as session:
                stmt = (
                    update(UserModel)
                    .where(UserModel.id.in_(pks))
                    .values(is_verified=True)
                )
                session.execute(stmt)
                session.commit()
            referer = request.headers.get("Referer")
        if referer:
            return RedirectResponse(referer)
        else:
            return RedirectResponse(
                request.url_for("admin:list", identity=self.identity)
            )
