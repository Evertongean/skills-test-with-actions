from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    name: str
    email: str
    phone: str
    address: str

    def contact_summary(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }


@dataclass
class Product:
    name: str
    quantity: int
    unit_price: float

    def subtotal(self):
        return self.quantity * self.unit_price


class PaymentService:
    accepted_methods = ("credit_card", "pix", "boleto")

    def charge(self, amount, payment_method):
        if payment_method not in self.accepted_methods:
            return {
                "method": payment_method,
                "amount": round(amount, 2),
                "status": "failed",
            }

        return {
            "method": payment_method,
            "amount": round(amount, 2),
            "status": "approved",
            "approved_at": datetime.utcnow().isoformat(),
        }


class NotificationService:
    def send_order_confirmation(self, customer, product, total):
        return {
            "email": customer.email,
            "phone": customer.phone,
            "message": (
                f"Olá {customer.name}, seu pedido de {product.quantity} unidade(s) "
                f"de {product.name} foi aprovado no valor de R$ {total:.2f}."
            ),
        }


class InvoiceService:
    def create_invoice(self, invoice_number, customer, product, subtotal, discount, tax, shipping, total):
        return {
            "number": f"NF-{invoice_number:04d}",
            "customer": customer.contact_summary(),
            "product": {
                "name": product.name,
                "quantity": product.quantity,
                "unit_price": product.unit_price,
            },
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "tax": round(tax, 2),
            "shipping": round(shipping, 2),
            "total": round(total, 2),
        }


class OrderProcessor:
    def __init__(self, payment_service=None, notification_service=None, invoice_service=None):
        self.payment_service = payment_service or PaymentService()
        self.notification_service = notification_service or NotificationService()
        self.invoice_service = invoice_service or InvoiceService()
        self.orders = []

    def process_order(self, customer, product, payment_method, coupon_code=None):
        errors = self._validate_order(customer, product)
        if errors:
            return {"status": "rejected", "errors": errors}

        subtotal = product.subtotal()
        discount = self._calculate_discount(subtotal, coupon_code)
        shipping = self._calculate_shipping(subtotal)
        tax = self._calculate_tax(subtotal, discount)
        total = subtotal - discount + tax + shipping

        payment = self.payment_service.charge(total, payment_method)
        if payment["status"] != "approved":
            return {
                "status": "payment_failed",
                "errors": ["Método de pagamento não aceito"],
                "payment": payment,
            }

        invoice = self.invoice_service.create_invoice(
            len(self.orders) + 1,
            customer,
            product,
            subtotal,
            discount,
            tax,
            shipping,
            total,
        )
        notification = self.notification_service.send_order_confirmation(customer, product, total)
        return self._save_order(customer, product, payment, invoice, notification, total)

    def _validate_order(self, customer, product):
        errors = []
        if not customer.name:
            errors.append("Nome do cliente é obrigatório")
        if not customer.email or "@" not in customer.email:
            errors.append("E-mail do cliente é inválido")
        if not customer.phone:
            errors.append("Telefone do cliente é obrigatório")
        if not customer.address:
            errors.append("Endereço do cliente é obrigatório")
        if not product.name:
            errors.append("Nome do produto é obrigatório")
        if product.quantity <= 0:
            errors.append("Quantidade deve ser maior que zero")
        if product.unit_price <= 0:
            errors.append("Preço unitário deve ser maior que zero")
        return errors

    def _calculate_discount(self, subtotal, coupon_code):
        discount = 0
        if coupon_code == "WELCOME10":
            discount = subtotal * 0.10
        return discount

    def _calculate_shipping(self, subtotal):
        shipping = 15
        if subtotal >= 200:
            shipping = 0
        return shipping

    def _calculate_tax(self, subtotal, discount):
        return (subtotal - discount) * 0.08

    def _save_order(self, customer, product, payment, invoice, notification, total):
        order = {
            "order_id": len(self.orders) + 1,
            "status": "approved",
            "customer": customer.contact_summary(),
            "product": {
                "name": product.name,
                "quantity": product.quantity,
                "unit_price": product.unit_price,
            },
            "payment": payment,
            "invoice": invoice,
            "notification": notification,
            "total": round(total, 2),
        }
        self.orders.append(order)
        return order
