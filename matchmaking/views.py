"""Module containing matchmaking views."""
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from matchmaking.filters import DealFilter
from matchmaking.models import Deal
from matchmaking.serializers import ListDealSerializer, CreateDealSerializer
from rest_framework.decorators import action

from matchmaking.usecases.accept_deal import AcceptDealUsecase


class ListCreateDealAPIView(ListCreateAPIView):
    """Fetch or create deals."""

    queryset = Deal.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("status",)
    filterset_class = DealFilter
    # permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Filter by deal status",
                type=openapi.TYPE_STRING,
                enum=[status.value for status in Deal.Status],
                required=True,
            ),
        ],
    )
    @action(methods=["GET"], detail=False)
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get list of deals."""
        return self.list(request, *args, **kwargs)

    def get_serializer_class(self):
        """Get serializer class."""
        if self.request.method == "POST":
            return CreateDealSerializer
        return ListDealSerializer


class AcceptDealAPIView(APIView):
    """Accept open deal."""

    queryset = Deal.objects.all()
    usecase = AcceptDealUsecase()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Accept open deal."""
        self.usecase.accept(deal_id=self.kwargs["pk"], profile=request.user.profile)
        return Response(data={"message": "success"}, status=status.HTTP_200_OK)
