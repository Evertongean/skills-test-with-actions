import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from order_processing import OrderProcessor  # noqa: E402


def test_process_order_successfully_processes_order():
    processor = OrderProcessor()

    order = processor.process_order(
        "Ana Lima",
        "ana@example.com",
        "85999990000",
        "Rua Central, 100",
        "Curso Python",
        2,
        100,
        "pix",
        coupon_code="WELCOME10",
    )

    assert order["status"] == "approved"
    assert order["total"] == pytest.approx(194.4)
    assert order["invoice"]["number"] == "NF-0001"
    assert len(processor.orders) == 1
    assert processor.payments[0]["status"] == "approved"
    assert processor.notifications[0]["email"] == "ana@example.com"


def test_process_order_rejects_invalid_data():
    processor = OrderProcessor()

    result = processor.process_order(
        "",
        "email-invalido",
        "",
        "",
        "",
        0,
        0,
        "pix",
    )

    assert result["status"] == "rejected"
    assert len(result["errors"]) == 7
    assert processor.audit_log[0]["event"] == "order_rejected"


def test_process_order_rejects_invalid_payment_method():
    processor = OrderProcessor()

    result = processor.process_order(
        "Ana Lima",
        "ana@example.com",
        "85999990000",
        "Rua Central, 100",
        "Curso Python",
        1,
        50,
        "cheque",
    )

    assert result["status"] == "payment_failed"
    assert result["payment"]["status"] == "failed"


def test_order_processor_also_handles_marketing_refunds_and_reports():
    processor = OrderProcessor()
    order = processor.process_order(
        "Ana Lima",
        "ana@example.com",
        "85999990000",
        "Rua Central, 100",
        "Curso Python",
        1,
        200,
        "credit_card",
    )

    marketing = processor.send_marketing_message(
        "Ana Lima",
        "ana@example.com",
        "85999990000",
        "Rua Central, 100",
        "Volta às aulas",
    )
    refund = processor.refund_order(order["order_id"], "Cliente desistiu")
    missing_refund = processor.refund_order(999, "Pedido inexistente")
    report = processor.generate_sales_report()

    assert marketing == "Campanha Volta às aulas enviada para Ana Lima"
    assert refund["status"] == "refunded"
    assert missing_refund["status"] == "not_found"
    assert report["total_orders"] == 1
    assert report["total_revenue"] == order["total"]
