# Data Flow - @carf/ui

## Fluxo de Dados

Componentes em @carf/ui seguem fluxo unidirecional de dados conforme [React data flow patterns](https://react.dev/learn/passing-data-deeply-with-context): **Props Down, Events Up**, onde componentes pais passam dados via props (state, configuration) e componentes filhos emitem eventos via callbacks (`onClick`, `onChange`, `onSubmit`) para notificar mudanças. State management é responsabilidade das aplicações consumidoras (GEOWEB/ADMIN), componentes da lib são [controlled components](https://react.dev/learn/sharing-state-between-components) stateless quando possível, mantendo apenas UI state interno (modals abertos, tabs ativas, accordions expandidos) via `useState` local, enquanto dados de domínio (Units, Holders, Communities) são sempre props controladas externamente. Para forms complexos, componentes exportam hooks customizados (`useUnitForm`, `useHolderValidation`) que encapsulam lógica de validação e state via React Hook Form + Zod schemas, retornando `{ control, errors, isSubmitting }` para o componente consumidor aplicar no JSX.

## Exemplo de Fluxo Completo

```tsx
// APP (GEOWEB) - State owner
function UnitsPage() {
  const [units, setUnits] = useState<Unit[]>([])
  const { data } = useQuery('units', () => api.units.list())

  useEffect(() => {
    if (data) setUnits(data)
  }, [data])

  const handleEdit = (unit: Unit) => {
    navigate(`/units/${unit.id}/edit`)
  }

  return (
    <UnitList
      units={units}              // Props down
      onEdit={handleEdit}        // Events up
      onDelete={handleDelete}
    />
  )
}

// COMPONENT (@carf/ui) - Stateless presentation
export function UnitList({ units, onEdit, onDelete }: UnitListProps) {
  return (
    <div className="grid gap-4">
      {units.map(unit => (
        <UnitCard
          key={unit.id}
          unit={unit}              // Props down
          onEdit={() => onEdit(unit)}  // Events up
          onDelete={() => onDelete(unit.id)}
        />
      ))}
    </div>
  )
}
```
