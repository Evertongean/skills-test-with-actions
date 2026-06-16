class Order:
    def __init__(
        self,
        calculator,
        payment_processor,
        email_service,
        invoice_service,
        inventory_service,
        audit_service,
        financial_report_service,
        history_service,
        shipping_service
    ):
        # TÓPICOS 6 e 7:
        # Order recebe os serviços prontos e apenas coordena o fluxo.
        self.calculator = calculator
        self.payment_processor = payment_processor
        self.email_service = email_service
        self.invoice_service = invoice_service
        self.inventory_service = inventory_service
        self.audit_service = audit_service
        self.financial_report_service = financial_report_service
        self.history_service = history_service
        self.shipping_service = shipping_service

    def process_order(self, customer, items, payment_type):
        # TÓPICO 3:
        # Uso do cálculo centralizado em OrderCalculator.
        total = self.calculator.calculate_total(items)

        # TÓPICO 5:
        # Uso do processador de pagamento no lugar de vários if/elif aqui.
        self.payment_processor.process_payment(payment_type)

        # TÓPICO 4:
        # O método recebe customer em vez de vários dados separados.
        self.print_customer_data(customer)

        # TÓPICOS 6 e 7:
        # As ações foram separadas em serviços específicos.
        self.email_service.send_email(customer.email, total)

        self.invoice_service.generate_invoice(
            customer.name,
            customer.cpf,
            total
        )

        self.inventory_service.update_inventory(items)

        self.audit_service.register_audit(customer.name, total)

        self.financial_report_service.generate_financial_report(total)

        self.history_service.save_history(customer.name, total)

        self.shipping_service.notify_shipping(customer.name)

    # TÓPICO 6:
    # Parte da lógica foi extraída para um método menor.
    def print_customer_data(self, customer):
        print(customer.name)
        print(customer.cpf)
        print(customer.email)
        print(customer.phone)
        print(customer.address.street)
        print(customer.address.number)
        print(customer.address.city)
        print(customer.address.state)