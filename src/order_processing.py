from datetime import datetime


class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.payments = []
        self.notifications = []
        self.invoices = []
        self.audit_log = []

    def process_order(
        self,
        customer_name,
        customer_email,
        customer_phone,
        customer_address,
        product_name,
        product_quantity,
        product_unit_price,
        payment_method,
        coupon_code=None,
    ):
        print("Dados do cliente")
        print(f"Nome: {customer_name}")
        print(f"E-mail: {customer_email}")
        print(f"Telefone: {customer_phone}")
        print(f"Endereço: {customer_address}")

        errors = []
        if not customer_name:
            errors.append("Nome do cliente é obrigatório")
        if not customer_email or "@" not in customer_email:
            errors.append("E-mail do cliente é inválido")
        if not customer_phone:
            errors.append("Telefone do cliente é obrigatório")
        if not customer_address:
            errors.append("Endereço do cliente é obrigatório")
        if not product_name:
            errors.append("Nome do produto é obrigatório")
        if product_quantity <= 0:
            errors.append("Quantidade deve ser maior que zero")
        if product_unit_price <= 0:
            errors.append("Preço unitário deve ser maior que zero")

        if errors:
            self.audit_log.append({
                "event": "order_rejected",
                "customer_email": customer_email,
                "errors": errors,
            })
            return {"status": "rejected", "errors": errors}

        print("Confirmando dados do cliente")
        print(f"Nome: {customer_name}")
        print(f"E-mail: {customer_email}")
        print(f"Telefone: {customer_phone}")
        print(f"Endereço: {customer_address}")

        subtotal = product_quantity * product_unit_price
        discount = 0
        if coupon_code == "WELCOME10":
            discount = subtotal * 0.10
        tax = (subtotal - discount) * 0.08
        shipping = 15
        if subtotal >= 200:
            shipping = 0
        total = subtotal - discount + tax + shipping

        payment_data = {
            "method": payment_method,
            "amount": round(total, 2),
            "status": "pending",
        }
        if payment_method not in ("credit_card", "pix", "boleto"):
            payment_data["status"] = "failed"
            self.payments.append(payment_data)
            self.audit_log.append({
                "event": "payment_failed",
                "customer_email": customer_email,
                "amount": round(total, 2),
            })
            return {
                "status": "payment_failed",
                "errors": ["Método de pagamento não aceito"],
                "payment": payment_data,
            }

        payment_data["status"] = "approved"
        payment_data["approved_at"] = datetime.utcnow().isoformat()
        self.payments.append(payment_data)

        print("Dados do cliente para notificação")
        print(f"Nome: {customer_name}")
        print(f"E-mail: {customer_email}")
        print(f"Telefone: {customer_phone}")
        print(f"Endereço: {customer_address}")

        notification_message = (
            f"Olá {customer_name}, seu pedido de {product_quantity} unidade(s) "
            f"de {product_name} foi aprovado no valor de R$ {total:.2f}."
        )
        self.notifications.append({
            "email": customer_email,
            "phone": customer_phone,
            "message": notification_message,
        })

        invoice = {
            "number": f"NF-{len(self.invoices) + 1:04d}",
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "customer_address": customer_address,
            "product_name": product_name,
            "quantity": product_quantity,
            "subtotal": round(subtotal, 2),
            "discount": round(discount, 2),
            "tax": round(tax, 2),
            "shipping": round(shipping, 2),
            "total": round(total, 2),
        }
        self.invoices.append(invoice)

        order = {
            "order_id": len(self.orders) + 1,
            "status": "approved",
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "customer_address": customer_address,
            "product_name": product_name,
            "quantity": product_quantity,
            "unit_price": product_unit_price,
            "payment": payment_data,
            "invoice": invoice,
            "total": round(total, 2),
        }
        self.orders.append(order)
        self.audit_log.append({
            "event": "order_saved",
            "order_id": order["order_id"],
            "customer_email": customer_email,
        })
        return order

    def send_marketing_message(self, customer_name, customer_email, customer_phone, customer_address, campaign_name):
        print("Dados do cliente")
        print(f"Nome: {customer_name}")
        print(f"E-mail: {customer_email}")
        print(f"Telefone: {customer_phone}")
        print(f"Endereço: {customer_address}")

        message = f"Campanha {campaign_name} enviada para {customer_name}"
        self.notifications.append({
            "email": customer_email,
            "phone": customer_phone,
            "message": message,
        })
        return message

    def refund_order(self, order_id, reason):
        for order in self.orders:
            if order["order_id"] == order_id:
                refund = {
                    "order_id": order_id,
                    "amount": order["total"],
                    "reason": reason,
                    "status": "refunded",
                }
                self.payments.append(refund)
                self.audit_log.append({"event": "order_refunded", "order_id": order_id})
                return refund

        refund = {"order_id": order_id, "reason": reason, "status": "not_found"}
        self.audit_log.append({"event": "refund_not_found", "order_id": order_id})
        return refund

    def generate_sales_report(self):
        total_orders = len(self.orders)
        total_revenue = sum(order["total"] for order in self.orders)
        total_notifications = len(self.notifications)
        return {
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "total_notifications": total_notifications,
            "generated_at": datetime.utcnow().isoformat(),
        }
