# TÓPICO 1:
# Remoção do método inadequado em Person.
# Antes, Person tinha generate_report(), mas Customer não usava esse método.
class Person:
    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf


# TÓPICO 4:
# Redução da lista longa de parâmetros.
# Os dados do cliente foram agrupados em uma classe.
class Customer(Person):
    def __init__(self, name, cpf, email, phone, address):
        super().__init__(name, cpf)
        self.email = email
        self.phone = phone
        self.address = address


# TÓPICO 4:
# Os dados de endereço foram agrupados em uma classe própria.
class Address:
    def __init__(self, street, number, city, state):
        self.street = street
        self.number = number
        self.city = city
        self.state = state