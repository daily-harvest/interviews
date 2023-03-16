from peewee import *

from app.db_connect import dh_db


class Orders(Model):
    order_id = AutoField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    user_id = IntegerField(index=True)
    billable_amount = DoubleField(null=True)
    charge_id = CharField(null=True, index=True)
    status = CharField(index=True)

    class Meta:
        database = dh_db
        db_table = 'orders'
