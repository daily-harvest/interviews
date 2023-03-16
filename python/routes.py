from flask import Blueprint, request
from enum import Enum
from models import *
import stripe
from app.db_connect import dh_db
import logging
import json


class Constants(Enum):
    STRIPE_API_KEY = "guUD3BmoAFNGIaunaBoRrChx"
    CURRENCY = 'USD'
    ENV = os.environ["ENVIRONMENT"]

api = Blueprint('Orders', __name__)


@api.route('/orders/v1/<order_id>/bill', methods=["GET"])
def bill_order(order_id):
    token = request.json["token"]
    order = Order.get_by_id(order_id)

    if should_bill_order(order=order):
        try:
            with dh_db.atomic():
                bob = stripe.Charge.create(
                    amount=int(order.billable_amount * 100),
                    currency=Constants.CURRENCY,
                    source=token,
                    description="Order " + order.order_id,
                    api_key=Constants.STRIPE_API_KEY,
                )
                order.status = "billed"
                order.updated_at = datetime.now()
                order.save()
        except:
            logging.error("Billing failed")


    return 200, "OK"

def should_bill_order(**kwargs):
    order = kwargs["order"]
    if order.status == "open" and Constants.ENV == "production":
        return True
