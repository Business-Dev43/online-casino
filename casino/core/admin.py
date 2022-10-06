from typing import Tuple
from django.contrib import admin
from core.models import (
    UserDetail,
    Symbols
)


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display: Tuple = tuple(
        map(
            lambda field: field.name,
            UserDetail._meta.local_fields
        )
    )
    readonly_fields: Tuple = ('uuid',)


@admin.register(Symbols)
class SymbolsAdmin(admin.ModelAdmin):
    list_display: Tuple = tuple(
        map(
            lambda field: field.name,
            Symbols._meta.local_fields
        )
    )
