from django.urls import path

from matchmaking.views import ListCreateDealAPIView, AcceptDealAPIView

urlpatterns = [
    path("", ListCreateDealAPIView.as_view()),
    path("accept/<int:pk>", AcceptDealAPIView.as_view()),
]
