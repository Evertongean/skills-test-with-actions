import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from order_processing import Customer, OrderProcessor, Product  # noqa: E402


def test_process_order_successfully_processes_order():
    processor = OrderProcessor()
    customer = Customer("Ana Lima", "ana@example.com", "85999990000", "Rua Central, 100")
    product = Product("Curso Python", 2, 100)

    order = processor.process_order(customer, product, "pix", coupon_code="WELCOME10")

    assert order["status"] == "approved"
    assert order["total"] == pytest.approx(194.4)
    assert order["customer"]["email"] == "ana@example.com"
    assert order["invoice"]["number"] == "NF-0001"
    assert order["payment"]["status"] == "approved"
    assert order["notification"]["email"] == "ana@example.com"


def test_process_order_rejects_invalid_data():
    processor = OrderProcessor()
    customer = Customer("", "email-invalido", "", "")
    product = Product("", 0, 0)

    result = processor.process_order(customer, product, "pix")

    assert result["status"] == "rejected"
    assert len(result["errors"]) == 7


def test_process_order_rejects_invalid_payment_method():
    processor = OrderProcessor()
    customer = Customer("Ana Lima", "ana@example.com", "85999990000", "Rua Central, 100")
    product = Product("Curso Python", 1, 50)

    result = processor.process_order(customer, product, "cheque")

    assert result["status"] == "payment_failed"
    assert result["payment"]["status"] == "failed"


def test_process_order_uses_free_shipping_for_large_subtotal():
    processor = OrderProcessor()
    customer = Customer("Ana Lima", "ana@example.com", "85999990000", "Rua Central, 100")
    product = Product("Curso Python", 1, 200)

    order = processor.process_order(customer, product, "credit_card")

    assert order["invoice"]["shipping"] == 0
    assert order["total"] == pytest.approx(216)
