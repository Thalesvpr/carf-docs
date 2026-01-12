# Key Concepts

@carf/ui fundamenta-se em três conceitos principais seguindo Atomic Design e Compound Components sendo Design Tokens CSS variables definindo tema visual customizáveis por aplicações consumidoras via globals.css permitindo trocar cores espaçamentos sem modificar código componentes, Atomic Design hierarquia composição onde Atoms (Button Input) combinam em Molecules (FormField Label Input Error) formando Organisms (LoginForm múltiplos FormFields Button) escalando Templates Pages aplicações consumidoras, e Compound Components padrão React onde componentes complexos exportam subcomponentes (Card.Header Card.Content Card.Footer) permitindo composição flexível separação responsabilidades implementado via Context API compartilhar state interno entre partes componente sem prop drilling.

---

**Última atualização:** 2026-01-11
