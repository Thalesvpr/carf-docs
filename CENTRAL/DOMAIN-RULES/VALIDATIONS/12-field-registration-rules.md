---
type: leaf
status: approved
updated: 2026-02-06
---

# Field Registration Rules

Regras de validacao especificas para cadastro em campo via aplicativo mobile. Garantem consistencia de dados, previnem erros comuns e implementam fluxos condicionais baseados no status da visita.

## Fluxo CPF-Primeiro

Cadastro de titular inicia obrigatoriamente pelo CPF. Demais campos do formulario permanecem desabilitados ate CPF ser validado. Validacao inclui: algoritmo de digitos verificadores da Receita Federal, unicidade no banco de dados do tenant, e verificacao de titular com multiplas unidades.

Enquanto CPF invalido ou duplicado, interface bloqueia preenchimento dos demais campos. Mensagem clara indica motivo do bloqueio. Usuario nao consegue salvar rascunho sem CPF valido.

## Regra de Unicidade de Titulo

Pessoa fisica identificada por CPF pode ser titular de no maximo uma unidade para fins de titulacao. Se CPF ja vinculado a outra unidade no sistema, cadastro e bloqueado com orientacao ao agente: informar ao morador que nao podera receber titulo desta unidade, sugerindo cadastrar familiar elegivel.

Excecao: cotitularidade e permitida quando mesma pessoa divide propriedade com conjuge ou companheiro em unica unidade. Vedado: mesma pessoa como titular principal de duas ou mais unidades distintas.

## Tres Categorias de Status (Distintas)

### A) Status de Atendimento

Indica o resultado da visita de campo. Determina obrigatoriedades condicionais do formulario.

| Status | Descricao | Formulario | Progressao |
|--------|-----------|------------|------------|
| Ausente | Ninguem atendeu | Minimo (localizacao + foto fachada) | Pode virar Presente |
| Nao quis | Morador recusou | Apenas observacao | Fim, nao retorna |
| Presente | Pessoa atendeu, cadastro em andamento | Completo | Pode virar Assinado |
| Assinado | Cadastro finalizado com assinatura | Completo + assinatura | Fim (status final) |

**Progressao tipica**: Ausente → Presente → Assinado

**Presente**: Formulario completo habilitado. Obrigatorio: foto de documento de identificacao (RG, CNH ou identidade nova).

**Ausente**: Campos pessoais do titular desabilitados. Cadastro minimo: status, numero unidade, endereco, foto fachada, observacao. Foto de fachada obrigatoria.

**Nao Quis**: Registra-se recusa sem retorno programado. Foto de fachada recomendada. Observacao descrevendo situacao obrigatoria.

**Assinado**: Cadastro completo validado com assinatura digital do titular. Status final do fluxo.

### B) Tipo de Ocupante

Classifica quem mora na unidade. Determina elegibilidade para titulacao.

| Tipo | Descricao | Elegivel para titulo? |
|------|-----------|----------------------|
| Possuidor | Quem tem posse do imovel | SIM |
| Locatario | Quem aluga o imovel | NAO (contata proprietario) |

### C) Tipo de Utilizacao do Imovel

Classifica o uso da unidade. Campo separado de status de atendimento.

| Tipo | Descricao |
|------|-----------|
| Residencial | Moradia |
| Comercio | Uso comercial |
| Misto | Residencia + comercio |
| Terreno vazio | Sem construcao |
| Nao habitado | Construcao abandonada ou em obras |

## Obrigatoriedade Condicional por Estado Civil

Se estado civil igual a Casado ou Uniao Estavel, campos do conjuge tornam-se obrigatorios: nome completo do conjuge, CPF do conjuge. Registro de uniao estavel deve indicar se reconhecida em cartorio ou nao.

## Regra do Campo "Outros"

Em qualquer dropdown com opcao "Outros" selecionada, campo texto livre torna-se obrigatorio. Nao permite salvar com "Outros" selecionado e campo descritivo vazio. Aplica-se a: profissao, escolaridade, tipo de edificacao, condicao de ocupacao.

## Campos de Filiacao

Substitui campos separados "Nome do Pai" e "Nome da Mae" por campo unico "Filiacao". Aceita um ou dois nomes. Nao exige identificacao de qual e pai ou mae, evitando constrangimentos e erros de preenchimento em documentos antigos.

**Campo opcional**: Existem pessoas registradas apenas com pai OU apenas com mae. Campo pode ficar vazio se titular nao possui ou nao sabe informar filiacao.

## Tempo de Moradia

Campo declaratorio indicando ha quanto tempo o titular mora no imovel. Aceita valores aproximados informados pelo morador (ex: "5 anos", "mais de 20 anos"). NAO e data especifica (mes/ano), pois nao exige precisao - morador raramente lembra data exata de quando se mudou.

## Campos de Ocupacao

Campo "Vinculo Empregaticio" renomeado para "Ocupacao". Valores possiveis: empregado formal, autonomo, aposentado, pensionista, desempregado, do lar, estudante, outros. Se "outros", campo texto obrigatorio.

Campo "Profissao" permanece separado com lista suspensa baseada em CBO (Classificacao Brasileira de Ocupacoes) simplificada. Busca por digitacao com autocomplete. Opcao "outros" com texto obrigatorio.

## Validacao de Documentos Fotograficos

Foto de fachada deve ser tirada exclusivamente pela camera do dispositivo. Acesso a galeria bloqueado para este tipo de documento. Preview obrigatorio antes de confirmar upload.

Foto de documento permite camera. OCR futuro para CNH e nova carteira de identidade preenchera campos automaticamente com confirmacao do usuario.

## Assinatura Digital do Titular

Status "Assinado" exige assinatura digital capturada no dispositivo. Coleta em tela landscape com canvas de desenho. Titular assina com o dedo diretamente na tela.

**Armazenamento**: Assinatura salva como imagem PNG no storage local, criptografada AES-256. Nunca armazenada na galeria do dispositivo. Campo `signature_path` no cadastro referencia arquivo criptografado.

**Vinculo**: Cada cadastro de titular possui campo `signature_path` (string, nullable). Status so pode transicionar para "Assinado" quando `signature_path` estiver preenchido com path valido.

**Validacao**:
- Canvas nao pode estar vazio ao confirmar
- Botao "Limpar" permite refazer
- Preview obrigatorio antes de salvar
- Orientacao forcada: landscape

**Modelo de dados**:
| Campo | Tipo | Descricao |
|-------|------|-----------|
| signature_path | String? | Caminho do arquivo PNG criptografado |
| signature_timestamp | DateTime | Momento da captura |
| signature_device_id | String | Identificador do dispositivo usado |
