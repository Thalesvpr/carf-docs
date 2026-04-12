---
type: leaf
status: review
updated: 2026-02-08
---

# Value Object Tests

Este documento detalha os testes unitarios de cada value object da camada de dominio. Cada value object e imutavel, validado no construtor e comparado por valor. Os testes cobrem criacao valida, rejeicao de dados invalidos e casos limites.

## Padrao Geral de Teste

Todos os testes de value objects seguem a mesma estrutura:

1. **Criacao valida** - instanciar com dados corretos e verificar propriedades
2. **Rejeicao de dados invalidos** - instanciar com dados incorretos e verificar que lanca DomainException
3. **Igualdade por valor** - dois value objects com mesmos dados devem ser iguais (Equals retorna verdadeiro, GetHashCode identico)
4. **Desigualdade** - dois value objects com dados diferentes devem ser diferentes
5. **Formatacao** - metodos de exibicao retornam o formato esperado

## CPF

A classe `CpfTests` valida o value object CPF, que encapsula a logica de validacao Mod-11 do CPF brasileiro.

### Algoritmo Mod-11

O CPF possui dois digitos verificadores calculados com pesos decrescentes. O primeiro digito usa pesos 10 a 2 sobre os 9 primeiros digitos. O segundo digito usa pesos 11 a 2 sobre os 10 primeiros digitos (incluindo o primeiro verificador). O resto da divisao por 11 determina o digito: se menor que 2, o digito e 0; caso contrario, e 11 menos o resto.

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| CPF valido sem mascara | `52998224725` | Instancia criada, Value igual a `52998224725` |
| CPF valido com mascara | `529.982.247-25` | Instancia criada, Value normalizado para `52998224725` |
| CPF com primeiro digito invalido | `52998224735` | Lanca DomainException com codigo `INVALID_CPF` |
| CPF com segundo digito invalido | `52998224726` | Lanca DomainException com codigo `INVALID_CPF` |
| Sequencia repetida 000.000.000-00 | `00000000000` | Lanca DomainException com codigo `INVALID_CPF` |
| Sequencia repetida 111.111.111-11 | `11111111111` | Lanca DomainException com codigo `INVALID_CPF` |
| Sequencia repetida 999.999.999-99 | `99999999999` | Lanca DomainException com codigo `INVALID_CPF` |
| Menos de 11 digitos | `5299822472` | Lanca DomainException com codigo `INVALID_CPF` |
| Mais de 11 digitos | `529982247250` | Lanca DomainException com codigo `INVALID_CPF` |
| Caracteres nao numericos | `5299822472A` | Lanca DomainException com codigo `INVALID_CPF` |
| Null | `null` | Lanca ArgumentNullException |
| String vazia | `""` | Lanca DomainException com codigo `INVALID_CPF` |
| Mascara parcial | `529.982247-25` | Instancia criada (aceita mascara parcial, normaliza) |
| Metodo Masked | `52998224725` | Retorna `***.982.247-**` (ofusca primeiro e ultimo blocos) |
| Igualdade por valor | Dois CPFs com `52998224725` | Equals retorna verdadeiro, HashCode identico |
| Desigualdade | `52998224725` vs `01234567890` | Equals retorna falso |

### Geracao de Dados com Bogus

O builder `CpfBuilder` gera CPFs validos usando o algoritmo Mod-11 completo. Utiliza `faker.Random.Number(100000000, 999999999)` para gerar os 9 primeiros digitos e calcula os verificadores. Para testes de CPF invalido, o builder possui o metodo `WithInvalidCheckDigit()` que inverte o ultimo digito.

## Email

A classe `EmailTests` valida o value object Email conforme RFC 5322 simplificada.

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| Email valido simples | `usuario@dominio.com` | Instancia criada, Value igual a entrada |
| Email valido com subdominio | `user@mail.dominio.com.br` | Instancia criada |
| Email valido com ponto no local | `nome.sobrenome@dominio.com` | Instancia criada |
| Email valido com mais e hifen | `user+tag@dom-inio.com` | Instancia criada |
| Sem arroba | `usuariodominio.com` | Lanca DomainException com codigo `INVALID_EMAIL` |
| Sem dominio | `usuario@` | Lanca DomainException com codigo `INVALID_EMAIL` |
| Sem local part | `@dominio.com` | Lanca DomainException com codigo `INVALID_EMAIL` |
| Dominio sem TLD | `usuario@dominio` | Lanca DomainException com codigo `INVALID_EMAIL` |
| Espacos no meio | `usu ario@dominio.com` | Lanca DomainException com codigo `INVALID_EMAIL` |
| Comprimento maximo 320 caracteres | 64 chars local + `@` + 255 chars domain | Instancia criada |
| Comprimento excede 320 caracteres | 65 chars local + `@` + 256 chars domain | Lanca DomainException com codigo `INVALID_EMAIL` |
| Null | `null` | Lanca ArgumentNullException |
| Normalizacao para minusculas | `Usuario@DOMINIO.Com` | Value igual a `usuario@dominio.com` |
| Igualdade por valor | Dois emails `a@b.com` | Equals retorna verdadeiro |

## GeoPolygon

A classe `GeoPolygonTests` valida o value object GeoPolygon que encapsula um poligono PostGIS com SRID 4326.

### Regras de Validacao

- O anel (ring) deve ser fechado: primeiro ponto igual ao ultimo ponto
- Minimo de 4 pontos (3 vertices + ponto de fechamento)
- Coordenadas dentro do intervalo valido: latitude entre -90 e 90, longitude entre -180 e 180
- O poligono nao pode ter auto-intersecao (self-intersection)
- SRID deve ser 4326 (WGS 84)

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| Poligono valido quadrado | 4 pontos formando quadrado + ponto de fechamento | Instancia criada, Geometry.IsValid verdadeiro |
| Poligono valido triangulo | 3 pontos formando triangulo + ponto de fechamento | Instancia criada |
| Anel nao fechado | Ultimo ponto diferente do primeiro | Lanca DomainException com codigo `INVALID_GEOMETRY` |
| Menos de 4 pontos | Apenas 2 pontos + fechamento | Lanca DomainException com codigo `INVALID_GEOMETRY` |
| Latitude fora do intervalo | Ponto com latitude 91 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Latitude negativa fora do intervalo | Ponto com latitude -91 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Longitude fora do intervalo | Ponto com longitude 181 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Longitude negativa fora do intervalo | Ponto com longitude -181 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Auto-intersecao (borboleta) | Poligono em forma de borboleta (lados cruzados) | Lanca DomainException com codigo `SELF_INTERSECTING_GEOMETRY` |
| SRID incorreto | Geometry com SRID 3857 | Lanca DomainException com codigo `INVALID_SRID` |
| Area calculada | Poligono de 100m x 100m em coordenadas conhecidas | Area aproximadamente 10000 m2 (tolerancia de 1%) |
| Centroid calculado | Poligono quadrado simetrico | Centroid no centro geometrico |
| Null | `null` | Lanca ArgumentNullException |
| Igualdade por valor | Dois poligonos com mesmas coordenadas | Equals retorna verdadeiro |

### Geracao de Dados com Bogus

O builder `GeoPolygonBuilder` utiliza coordenadas base na regiao de Brasilia (latitude -15.7, longitude -47.9) e gera poligonos regulares (quadrados) de tamanho configuravel. O metodo `WithSelfIntersection()` inverte dois vertices para criar auto-intersecao. O metodo `WithAreaApprox(double m2)` ajusta o tamanho do poligono para aproximar a area desejada.

## GeoPoint

A classe `GeoPointTests` valida o value object GeoPoint que encapsula um ponto PostGIS com SRID 4326.

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| Ponto valido | Latitude -15.7801, Longitude -47.9292 | Instancia criada, SRID igual a 4326 |
| Latitude limite superior | Latitude 90.0 | Instancia criada |
| Latitude limite inferior | Latitude -90.0 | Instancia criada |
| Longitude limite superior | Longitude 180.0 | Instancia criada |
| Longitude limite inferior | Longitude -180.0 | Instancia criada |
| Latitude acima do limite | Latitude 90.1 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Latitude abaixo do limite | Latitude -90.1 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Longitude acima do limite | Longitude 180.1 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| Longitude abaixo do limite | Longitude -180.1 | Lanca DomainException com codigo `INVALID_COORDINATES` |
| SRID automatico 4326 | Ponto sem SRID explicito | SRID igual a 4326 |
| Precisao de 8 casas decimais | -15.78012345 | Precisao mantida |
| Distancia entre dois pontos | Dois pontos conhecidos | DistanceTo retorna valor esperado em metros (tolerancia 0.1%) |
| Igualdade por valor | Dois pontos identicos | Equals retorna verdadeiro |
| Desigualdade por precisao | Pontos diferindo na 8a casa decimal | Equals retorna falso |

## Address

A classe `AddressTests` valida o value object Address que encapsula um endereco brasileiro.

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| Endereco completo | Rua A, 123, Apto 4, Centro, Brasilia, DF | FullAddress concatena corretamente todos os campos |
| Sem complemento | Rua A, 123, null, Centro, Brasilia, DF | FullAddress omite complemento sem virgula extra |
| Sem numero | Rua A, S/N, null, Centro, Brasilia, DF | FullAddress exibe S/N como numero |
| CEP formatado | `70000000` | Formatted retorna `70000-000` |
| CEP invalido (menos de 8 digitos) | `7000000` | Lanca DomainException com codigo `INVALID_CEP` |
| UF invalida | `XX` | Lanca DomainException com codigo `INVALID_UF` |
| UF valida todas as 27 | Cada UF brasileira | Todas instanciam corretamente |
| Logradouro vazio | `""` | Lanca DomainException com codigo `INVALID_ADDRESS` |
| Cidade vazia | `""` | Lanca DomainException com codigo `INVALID_ADDRESS` |
| Igualdade por valor | Dois enderecos identicos | Equals retorna verdadeiro |

### Geracao de Dados com Bogus

O builder `AddressBuilder` utiliza `faker.Address.StreetName()`, `faker.Address.BuildingNumber()`, `faker.Address.City()` e seleciona uma UF aleatoria da lista valida. O metodo `WithoutComplemento()` define complemento como null para testes de formatacao.

## PhoneNumber

A classe `PhoneNumberTests` valida o value object PhoneNumber para numeros brasileiros.

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| Celular valido com +55 | `+5561999887766` | Instancia criada, IsMobile verdadeiro |
| Fixo valido com +55 | `+556133445566` | Instancia criada, IsMobile falso |
| Celular sem codigo pais | `61999887766` | Normalizado para `+5561999887766` |
| DDD invalido | `+5500999887766` | Lanca DomainException com codigo `INVALID_PHONE` |
| DDD valido 11 (SP) | `+5511999887766` | Instancia criada |
| DDD valido 99 (MA) | `+5599999887766` | Instancia criada |
| Celular sem nono digito | `+556199988776` | Lanca DomainException com codigo `INVALID_PHONE` |
| Caracteres nao numericos | `+55(61)99988-7766` | Normalizado para `+5561999887766` (aceita mascara) |
| Null | `null` | Lanca ArgumentNullException |
| String vazia | `""` | Lanca DomainException com codigo `INVALID_PHONE` |
| Formatted (celular) | `+5561999887766` | Retorna `(61) 99988-7766` |
| Formatted (fixo) | `+556133445566` | Retorna `(61) 3344-5566` |
| Igualdade por valor | Dois phones identicos | Equals retorna verdadeiro |

## CREA

A classe `CreaTests` valida o value object CREA (Conselho Regional de Engenharia e Agronomia).

### Cenarios de Teste

| Cenario | Entrada | Assertion |
|---------|---------|-----------|
| CREA valido | `123456/D-DF` | Instancia criada, Number igual a `123456`, UF igual a `DF` |
| CREA valido com tipo diferente | `789012/D-SP` | Instancia criada |
| Formato sem barra | `123456DDF` | Lanca DomainException com codigo `INVALID_CREA` |
| UF invalida | `123456/D-XX` | Lanca DomainException com codigo `INVALID_CREA` |
| Numero com letras | `12A456/D-DF` | Lanca DomainException com codigo `INVALID_CREA` |
| Null | `null` | Lanca ArgumentNullException |
| String vazia | `""` | Lanca DomainException com codigo `INVALID_CREA` |
| Igualdade por valor | Dois CREAs identicos | Equals retorna verdadeiro |
| Desigualdade por UF | Mesmo numero, UFs diferentes | Equals retorna falso |

## Tabela Resumo

| Value Object | Classe de Teste | Cenarios Validos | Cenarios Invalidos | Cenarios Edge Case | Total |
|--------------|----------------|------------------|--------------------|--------------------|-------|
| CPF | CpfTests | 3 | 7 | 5 | 15 |
| Email | EmailTests | 5 | 6 | 3 | 14 |
| GeoPolygon | GeoPolygonTests | 4 | 5 | 4 | 13 |
| GeoPoint | GeoPointTests | 5 | 4 | 4 | 13 |
| Address | AddressTests | 4 | 3 | 3 | 10 |
| PhoneNumber | PhoneNumberTests | 5 | 4 | 4 | 13 |
| CREA | CreaTests | 2 | 4 | 3 | 9 |

## Assertions com FluentAssertions

Padroes de assertion utilizados nos testes de value objects:

- **Criacao valida**: `var cpf = CPF.Create("52998224725"); cpf.Value.Should().Be("52998224725");`
- **Excecao esperada**: `var act = () => CPF.Create("00000000000"); act.Should().Throw<DomainException>().WithMessage("*INVALID_CPF*");`
- **Igualdade**: `cpf1.Should().Be(cpf2);`
- **Desigualdade**: `cpf1.Should().NotBe(cpf2);`
- **Propriedade booleana**: `phone.IsMobile.Should().BeTrue();`
- **Formatacao**: `cpf.Masked.Should().Be("***.982.247-**");`

## Referencias Cruzadas

- Definicao dos value objects: `DOMAIN/VALUE-OBJECTS/`
- Testes de entidades que usam esses VOs: `TESTS/UNIT/01-domain-unit-tests.md`
- Validators que referenciam VOs: `APPLICATION/VALIDATORS/`
