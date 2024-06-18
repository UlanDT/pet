import pytest

from matchmaking.models import Deal
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_with_client(token):
    # arrange
    Deal.objects.create(token=token, open_price=500)

    # act
    response = client.get('/deals/')

    # assert
    assert response.status_code == 200
