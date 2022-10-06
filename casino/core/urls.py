from django.urls import path
from core.views import (
    StartGame,
    CreateUserSession,
    casinoView,
    RollView,
    CloseSessionView
)

urlpatterns = [
    path("", StartGame.as_view(), name="start"),
    path("create_session", CreateUserSession.as_view(), name="create_session"),
    path("casino", casinoView.as_view(), name="casino"),
    path("roll", RollView.as_view(), name="roll"),
    path("close_session", CloseSessionView.as_view(), name="close_session"),
]
