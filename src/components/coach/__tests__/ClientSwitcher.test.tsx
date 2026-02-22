import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { ClientSwitcher } from '../ClientSwitcher'
import { mockClients } from '../__mocks__/clients'
import { Client } from '../../../types/calendar'

describe('ClientSwitcher', () => {
  // Scenario: Display all clients in the switcher
  describe('Scenario: Display all clients in the switcher', () => {
    it('CMP-13: renders all client names as selectable options', () => {
      const onSelect = vi.fn()
      render(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[0].id}
          onSelect={onSelect}
        />
      )
      mockClients.forEach((client) => {
        expect(screen.getByText(client.name)).toBeInTheDocument()
      })
    })

    it('CMP-14: first client option is marked as selected by default', () => {
      const onSelect = vi.fn()
      render(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[0].id}
          onSelect={onSelect}
        />
      )
      const firstOption = screen.getByTestId(`client-option-${mockClients[0].id}`)
      expect(firstOption).toHaveAttribute('aria-selected', 'true')
    })

    it('CMP-15: non-selected clients have aria-selected false', () => {
      const onSelect = vi.fn()
      render(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[0].id}
          onSelect={onSelect}
        />
      )
      const secondOption = screen.getByTestId(`client-option-${mockClients[1].id}`)
      expect(secondOption).toHaveAttribute('aria-selected', 'false')
    })
  })

  // Scenario: Switch to a different client
  describe('Scenario: Switch to a different client', () => {
    it('CMP-16: clicking a client calls onSelect with that client id', () => {
      const onSelect = vi.fn()
      render(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[0].id}
          onSelect={onSelect}
        />
      )
      const secondOption = screen.getByTestId(`client-option-${mockClients[1].id}`)
      fireEvent.click(secondOption)
      expect(onSelect).toHaveBeenCalledOnce()
      expect(onSelect).toHaveBeenCalledWith(mockClients[1].id)
    })

    it('CMP-17: selected client pill reflects updated selectedClientId prop', () => {
      const onSelect = vi.fn()
      const { rerender } = render(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[0].id}
          onSelect={onSelect}
        />
      )
      // Initially Client A is selected
      expect(screen.getByTestId(`client-option-${mockClients[0].id}`)).toHaveAttribute(
        'aria-selected',
        'true'
      )
      // After parent updates the prop to Client B
      rerender(
        <ClientSwitcher
          clients={mockClients}
          selectedClientId={mockClients[1].id}
          onSelect={onSelect}
        />
      )
      expect(screen.getByTestId(`client-option-${mockClients[1].id}`)).toHaveAttribute(
        'aria-selected',
        'true'
      )
      expect(screen.getByTestId(`client-option-${mockClients[0].id}`)).toHaveAttribute(
        'aria-selected',
        'false'
      )
    })
  })

  // Scenario: Single client (no roster)
  describe('Scenario: Single client', () => {
    it('CMP-18: renders a single client as selected when only one exists', () => {
      const singleClient: Client[] = [mockClients[0]]
      const onSelect = vi.fn()
      render(
        <ClientSwitcher
          clients={singleClient}
          selectedClientId={singleClient[0].id}
          onSelect={onSelect}
        />
      )
      expect(screen.getByText(singleClient[0].name)).toBeInTheDocument()
      expect(screen.getByTestId(`client-option-${singleClient[0].id}`)).toHaveAttribute(
        'aria-selected',
        'true'
      )
    })
  })

  // Scenario: client-switcher container has correct role
  it('CMP-19: container has tablist role and aria-label', () => {
    const onSelect = vi.fn()
    render(
      <ClientSwitcher
        clients={mockClients}
        selectedClientId={mockClients[0].id}
        onSelect={onSelect}
      />
    )
    const switcher = screen.getByTestId('client-switcher')
    expect(switcher).toHaveAttribute('role', 'tablist')
    expect(switcher).toHaveAttribute('aria-label', 'Client selector')
  })
})
