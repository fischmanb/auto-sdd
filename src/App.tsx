import { useState } from 'react'
import { WeekView } from './components/calendar/WeekView'
import { ClientSwitcher } from './components/coach/ClientSwitcher'
import { mockClients } from './components/coach/__mocks__/clients'

export default function App() {
  const [selectedClientId, setSelectedClientId] = useState(mockClients[0].id)

  const selectedClient = mockClients.find((c) => c.id === selectedClientId) ?? mockClients[0]

  return (
    <div className="min-h-screen bg-surface p-4 sm:p-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">ADHD Calendar</h1>
      <div className="mb-4">
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={selectedClientId}
          onSelect={setSelectedClientId}
        />
      </div>
      <WeekView blocks={selectedClient.blocks} weekOf={new Date(2026, 1, 16)} />
    </div>
  )
}
