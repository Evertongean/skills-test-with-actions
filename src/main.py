from models import Address, Customer

from services import (
    OrderCalculator,
    PaymentProcessor,
    EmailService,
    InvoiceService,
    InventoryService,
    AuditService,
    FinancialReportService,
    HistoryService,
    ShippingService
)

from order import Order


# TÓPICO 4:
# Criação do objeto Address, agrupando dados de endereço.
address = Address(
    street="Rua A",
    number="123",
    city="Uiraúna",
    state="PB"
)


# TÓPICO 4:
# Criação do objeto Customer, agrupando dados do cliente.
customer = Customer(
    name="João Silva",
    cpf="123.456.789-00",
    email="joao@email.com",
    phone="83999999999",
    address=address
)


items = [
    {"price": 10, "quantity": 2},
    {"price": 5, "quantity": 3}
]


# TÓPICOS 6 e 7:
# Os serviços são criados separadamente e passados para Order.
order = Order(
    calculator=OrderCalculator(),
    payment_processor=PaymentProcessor(),
    email_service=EmailService(),
    invoice_service=InvoiceService(),
    inventory_service=InventoryService(),
    audit_service=AuditService(),
    financial_report_service=FinancialReportService(),
    history_service=HistoryService(),
    shipping_service=ShippingService()
)


# TÓPICO 4:
# process_order agora recebe poucos parâmetros:
# customer, items e payment_type.
order.process_order(
    customer=customer,
    items=items,
    payment_type="PIX"
)