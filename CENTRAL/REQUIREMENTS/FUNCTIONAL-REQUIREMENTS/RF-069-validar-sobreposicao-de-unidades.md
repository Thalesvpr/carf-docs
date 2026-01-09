---
modules: [GEOWEB]
epic: units
---

# RF-069: Validar Sobreposição de Unidades

O sistema deve detectar automaticamente sobreposições geométricas entre unidades habitacionais ao salvar novo cadastro ou editar geometria existente, onde validação espacial utiliza operadores PostGIS (ST_Intersects ST_Overlaps) consultando índices geométricos para identificar unidades cuja geometria se sobrepõe à unidade sendo salva. Quando sobreposição é detectada, o sistema apresenta alerta visual destacando o problema e listando identificadores e endereços das unidades conflitantes, permitindo que usuário verifique se sobreposição é legítima (edificação verticalizada com múltiplas unidades) ou erro de cadastro que precisa correção. A validação não bloqueia salvamento mas registra warning no log de auditoria documentando que unidade foi salva mesmo com sobreposição detectada, garantindo flexibilidade para casos válidos de sobreposição enquanto mantém rastreabilidade de situações anômalas. Interface oferece visualização das unidades sobrepostas diretamente no mapa destacando área de interseção em cor diferenciada, facilitando compreensão espacial do conflito e permitindo ajuste preciso das geometrias para resolver sobreposição quando esta resultar de erro de desenho ou posicionamento inadequado dos polígonos cadastrados.

---

**Última atualização:** 2025-12-30
