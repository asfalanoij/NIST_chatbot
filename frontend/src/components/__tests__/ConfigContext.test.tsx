import { render, screen, waitFor } from '@testing-library/react'
import { ConfigProvider, useConfig } from '../../context/ConfigContext'

const mockAgents = [
  { id: 'NIST_SPECIALIST', name: 'NIST Controls Specialist', description: 'desc', icon: 'Shield', details: ['d1'] },
  { id: 'AUDIT_SPECIALIST', name: 'Audit Specialist', description: 'desc', icon: 'Search', details: ['d1'] },
]

const mockCrossmap = [
  { nist_id: 'AC-2', nist_title: 'Account Management', nist_family: 'AC', iso27001: [], iso27001_titles: [], csf2: [], csf2_titles: [], iso27005: [], iso27005_titles: [] },
]

function TestConsumer() {
  const { agents, crossmap, loading, error } = useConfig()
  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  return (
    <div>
      <span data-testid="agent-count">{agents.length}</span>
      <span data-testid="crossmap-count">{crossmap.length}</span>
    </div>
  )
}

describe('ConfigContext', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('provides agents after fetch', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      const urlStr = typeof url === 'string' ? url : url.toString()
      if (urlStr.includes('/config/agents')) {
        return Promise.resolve(new Response(JSON.stringify(mockAgents), { status: 200 }))
      }
      return Promise.resolve(new Response(JSON.stringify(mockCrossmap), { status: 200 }))
    })

    render(
      <ConfigProvider>
        <TestConsumer />
      </ConfigProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('agent-count')).toHaveTextContent('2')
    })
  })

  it('provides crossmap after fetch', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      const urlStr = typeof url === 'string' ? url : url.toString()
      if (urlStr.includes('/config/agents')) {
        return Promise.resolve(new Response(JSON.stringify(mockAgents), { status: 200 }))
      }
      return Promise.resolve(new Response(JSON.stringify(mockCrossmap), { status: 200 }))
    })

    render(
      <ConfigProvider>
        <TestConsumer />
      </ConfigProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('crossmap-count')).toHaveTextContent('1')
    })
  })

  it('sets error on fetch failure', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => {
      return Promise.resolve(new Response('', { status: 500 }))
    })

    render(
      <ConfigProvider>
        <TestConsumer />
      </ConfigProvider>
    )

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument()
    })
  })
})
