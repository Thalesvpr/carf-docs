---
type: leaf
status: review
updated: 2026-02-08
---

# BaseValueObject

Classe base abstrata que todos os value objects do dominio herdam, fornecendo implementacao padrao de igualdade por valor e imutabilidade garantida por design. Diferentemente de entidades como Unit ou Holder que sao comparadas por identidade (Id), value objects sao comparados exclusivamente pelos valores de todos os seus campos. Dois objetos Cpf com os mesmos 11 digitos sao considerados iguais mesmo sendo instancias distintas em memoria.

A imutabilidade e garantida por convencao: todos os campos sao propriedades somente-leitura inicializadas pelo construtor, sem setters publicos. Apos criado, o estado de um value object jamais muda. Caso um valor diferente seja necessario, uma nova instancia deve ser criada.

## Metodos Principais

| Metodo | Retorno | Descricao |
|--------|---------|----------|
| Equals(object) | bool | Sobrescrito para comparar valores dos campos ao inves de referencia de memoria. |
| GetHashCode() | int | Sobrescrito retornando hash baseado nos valores, permitindo uso em dicionarios e conjuntos. |
| operator == | bool | Delegado para Equals, fornecendo sintaxe natural de comparacao. |
| operator \!= | bool | Negacao de ==. |
| GetEqualityComponents() | IEnumerable | Metodo abstrato que subclasses implementam retornando campos que participam da igualdade. |

## Regras de Validacao

| Regra | Descricao |
|-------|----------|
| Imutabilidade | Todos os campos devem ser readonly ou get-only. Nenhum setter publico e permitido. |
| Comparacao por valor | Duas instancias com campos identicos devem ser consideradas iguais. |
| Hash consistente | Instancias iguais devem produzir mesmo hash code para uso em HashSet e Dictionary. |
| Sem identidade | Value objects nao possuem Id proprio; sua identidade e definida pelos valores. |

## Subclasses no Dominio

BaseValueObject serve como base para todos os value objects incluindo Cpf, Email, PhoneNumber, GeoPolygon, GeoPoint, Address e enums especializados como UnitStatus, CommunityType e TeamRole. Essa hierarquia garante comportamento consistente de comparacao e substituibilidade em todo o dominio.
