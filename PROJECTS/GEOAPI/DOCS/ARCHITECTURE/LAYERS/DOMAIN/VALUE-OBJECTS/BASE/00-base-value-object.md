# BaseValueObject

Classe base abstrata que todos os value objects herdam, fornecendo implementação padrão de igualdade por valor ao invés de referência e imutabilidade garantida através de design. Diferentemente de entidades que são comparadas por Id (identidade), value objects são comparados pelos valores de todos os seus campos, de forma que dois CPF com mesmos 11 dígitos são considerados o mesmo value object mesmo sendo instâncias diferentes na memória.

Métodos principais incluem Equals(object) sobrescrito para comparar valores dos campos ao invés de referência de memória, GetHashCode() sobrescrito retornando hash baseado nos valores permitindo uso correto em dicionários e conjuntos, operadores == e != sobrescritos delegando para Equals() fornecendo sintaxe natural de comparação, e GetEqualityComponents() abstrato que subclasses implementam retornando IEnumerable dos campos que participam da igualdade. Garante imutabilidade através de convenção (todos os campos são readonly ou get-only properties, sem setters públicos, construtor valida e inicializa estado que nunca muda).

Usado como base para todos os value objects do domínio incluindo Cpf, Email, GeoPolygon, Address e enums especializados garantindo comportamento consistente de comparação por valor e substituibilidade, permitindo que Unit com Address("Rua A, 10") seja considerado igual a outro Unit com Address("Rua A", 10") se todos os componentes do endereço forem idênticos.

---

**Última atualização:** 2026-01-12
