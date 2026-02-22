import { ClientSwitcherProps } from '../../types/calendar'

export function ClientSwitcher({ clients, selectedClientId, onSelect }: ClientSwitcherProps) {
  return (
    <div
      data-testid="client-switcher"
      className="flex gap-2 flex-wrap"
      role="tablist"
      aria-label="Client selector"
    >
      {clients.map((client) => {
        const isSelected = client.id === selectedClientId
        return (
          <button
            key={client.id}
            data-testid={`client-option-${client.id}`}
            role="tab"
            aria-selected={isSelected}
            onClick={() => onSelect(client.id)}
            className={
              isSelected
                ? 'px-4 py-2 rounded-full text-sm font-medium bg-blue-600 text-white border border-blue-600'
                : 'px-4 py-2 rounded-full text-sm font-medium bg-white text-gray-800 border border-gray-300 hover:border-blue-400'
            }
          >
            {client.name}
          </button>
        )
      })}
    </div>
  )
}
