# TÓPICO 2:
# Separação da antiga ReportService.
# Agora cada classe tem uma responsabilidade mais específica.
class CustomerPrinter:
    def print_customer(self, customer):
        print(customer.name)
        print(customer.cpf)


# TÓPICO 2:
# Classe específica para validação do cliente.
class CustomerValidator:
    def validate_customer(self, customer):
        print(customer.name)
        print(customer.cpf)


# TÓPICO 2:
# Classe específica para exportação do cliente.
class CustomerExporter:
    def export_customer(self, customer):
        print(customer.name)
        print(customer.cpf)


# TÓPICO 3:
# Eliminação de código duplicado.
# O cálculo do total foi centralizado neste método.
class OrderCalculator:
    def calculate_total(self, items):
        total = 0

        for item in items:
            total += item["price"] * item["quantity"]

        return total


# TÓPICO 5:
# Substituição dos vários if/elif por um dicionário.
class PaymentProcessor:
    def process_payment(self, payment_type):
        payment_messages = {
            "PIX": "Pagamento PIX",
            "CARD": "Pagamento Cartão",
            "BOLETO": "Pagamento Boleto"
        }

        if payment_type in payment_messages:
            print(payment_messages[payment_type])


# TÓPICOS 6 e 7:
# Divisão do método process_order e aplicação da responsabilidade única.
# Cada serviço abaixo cuida de uma tarefa específica.
class EmailService:
    def send_email(self, email, total):
        print("Email enviado")


class InvoiceService:
    def generate_invoice(self, name, cpf, total):
        print("NF gerada")


class InventoryService:
    def update_inventory(self, items):
        print("Estoque atualizado")


class AuditService:
    def register_audit(self, name, total):
        print("Auditoria registrada")


class FinancialReportService:
    def generate_financial_report(self, total):
        print("Relatório financeiro")


class HistoryService:
    def save_history(self, name, total):
        print("Histórico salvo")


class ShippingService:
    def notify_shipping(self, name):
        print("Transportadora notificada")