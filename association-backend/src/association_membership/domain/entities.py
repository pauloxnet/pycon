from __future__ import annotations

import logging
from datetime import datetime
from enum import Enum
from typing import Any, List

import ormar
import sqlalchemy
from pydantic import PrivateAttr

from src.customers.domain.entities import Customer
from src.database.db import BaseMeta

logger = logging.getLogger(__name__)


class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELED = "canceled"

    def __str__(self) -> str:
        return str.__str__(self)


class Subscription(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscriptions"

    id: int = ormar.Integer(primary_key=True)
    customer: Customer = ormar.ForeignKey(Customer, nullable=False)
    stripe_subscription_id: str = ormar.String(nullable=False, max_length=256)
    status: SubscriptionStatus = ormar.String(
        max_length=20,
        choices=list(SubscriptionStatus),
        default=SubscriptionStatus.PENDING,
        nullable=False,
    )

    _add_invoice: List[SubscriptionInvoice] = PrivateAttr(default_factory=list)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._add_invoice = []

    def add_invoice(self, payment: SubscriptionInvoice):
        self._add_invoice.append(payment)

    def mark_as_canceled(self):
        self._change_state(SubscriptionStatus.CANCELED)

    def mark_as_active(self):
        self._change_state(SubscriptionStatus.ACTIVE)

    @property
    def is_active(self) -> bool:
        return self.status == SubscriptionStatus.ACTIVE

    def _change_state(self, to: SubscriptionStatus):
        logger.info("Switching subscription from status %s to %s", self.status, to)
        self.status = to


class InvoiceStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    PAID = "paid"
    UNCOLLECTIBLE = "uncollectible"
    VOID = "void"

    def __str__(self) -> str:
        return str.__str__(self)


class DateTimeWithTimeZone(ormar.DateTime):
    @classmethod
    def get_column_type(cls, **kwargs: Any) -> Any:
        return sqlalchemy.DateTime(timezone=True)


class SubscriptionInvoice(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscription_invoices"

    id: int = ormar.Integer(primary_key=True)
    status: InvoiceStatus = ormar.String(
        max_length=50,
        default=InvoiceStatus.DRAFT,
        server_default=InvoiceStatus.DRAFT,
        choices=list(InvoiceStatus),
    )
    subscription: Subscription = ormar.ForeignKey(
        Subscription, nullable=False, related_name="invoices"
    )
    payment_date: datetime = DateTimeWithTimeZone()
    period_start: datetime = DateTimeWithTimeZone()
    period_end: datetime = DateTimeWithTimeZone()
    stripe_invoice_id: str = ormar.String(max_length=256)
    invoice_pdf: str = ormar.Text()