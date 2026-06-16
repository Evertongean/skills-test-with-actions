class Person:
    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf

    def generate_report(self):
        print("Generic report")


class Customer(Person):
    def generate_report(self):
        raise NotImplementedError(
            "Customer should not generate reports"
        )


class ReportService:

    def print_customer(self, customer):
        print(customer.name)
        print(customer.cpf)

    def validate_customer(self, customer):
        print(customer.name)
        print(customer.cpf)

    def export_customer(self, customer):
        print(customer.name)
        print(customer.cpf)


class Order:

    def process_order(
        self,
        name,
        cpf,
        email,
        phone,
        street,
        number,
        city,
        state,
        items,
        payment_type
    ):

        total = 0

        for item in items:
            total += item["price"] * item["quantity"]

        # cálculo repetido
        total2 = 0

        for item in items:
            total2 += item["price"] * item["quantity"]

        if payment_type == "PIX":
            print("Pagamento PIX")
        elif payment_type == "CARD":
            print("Pagamento Cartão")
        elif payment_type == "BOLETO":
            print("Pagamento Boleto")

        print(name)
        print(cpf)
        print(email)
        print(phone)
        print(street)
        print(number)
        print(city)
        print(state)

        self.send_email(email, total)

        self.generate_invoice(name, cpf, total)

        self.update_inventory(items)

        self.register_audit(name, total)

        self.generate_financial_report(total)

        self.save_history(name, total)

        self.notify_shipping(name)

    def send_email(self, email, total):
        print("Email enviado")

    def generate_invoice(self, name, cpf, total):
        print("NF gerada")

    def update_inventory(self, items):
        print("Estoque atualizado")

    def register_audit(self, name, total):
        print("Auditoria registrada")

    def generate_financial_report(self, total):
        print("Relatório financeiro")

    def save_history(self, name, total):
        print("Histórico salvo")

    def notify_shipping(self, name):
        print("Transportadora notificada")