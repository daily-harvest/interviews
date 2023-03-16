from models import *
from unittest.mock import patch, Mock
import json


mock_order = Mock(order_id=1)


@patch('routes.Order.get_by_id', mock_order)
@patch('routes.stripe.Charge.create')
def test_bill_order(client):
    response = client.get(
        '/orders/v1/1/bill',
        data=json.dumps({"token": "abc"}),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
