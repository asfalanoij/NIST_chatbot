import { render, screen, waitFor } from '@testing-library/react'
import App from '../../App'
import { ConfigProvider } from '../../context/ConfigContext'

const mockAgents = [
  { id: 'NIST_SPECIALIST', name: 'NIST Controls Specialist', description: 'desc', icon: 'Shield', details: ['d1'] },
]

const mockCrossmap = [
  { nist_id: 'AC-2', nist_title: 'Account Management', nist_family: 'AC', iso27001: [], iso27001_titles: [], csf2: [], csf2_titles: [], iso27005: [], iso27005_titles: [] },
]

describe('App', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockImplementation((url) => {
      const urlStr = typeof url === 'string' ? url : url.toString()
      if (urlStr.includes('/config/agents')) {
        return Promise.resolve(new Response(JSON.stringify(mockAgents), { status: 200 }))
      }
      if (urlStr.includes('/config/crossmap')) {
        return Promise.resolve(new Response(JSON.stringify(mockCrossmap), { status: 200 }))
      }
      if (urlStr.includes('/health')) {
        return Promise.resolve(new Response(JSON.stringify({ status: 'healthy', llm_backend: 'gemini' }), { status: 200 }))
      }
      return Promise.resolve(new Response('{}', { status: 200 }))
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders without crashing', async () => {
    render(
      <ConfigProvider>
        <App />
      </ConfigProvider>
    )
    // App should mount without throwing
    await waitFor(() => {
      expect(document.querySelector('.bg-brand-dark')).toBeInTheDocument()
    })
  })

  it('renders quick prompt buttons', async () => {
    render(
      <ConfigProvider>
        <App />
      </ConfigProvider>
    )
    await waitFor(() => {
      expect(screen.getByText('Explain AC-2')).toBeInTheDocument()
    })
  })

  it('renders system status', async () => {
    render(
      <ConfigProvider>
        <App />
      </ConfigProvider>
    )
    await waitFor(() => {
      expect(screen.getByText(/System Ready|Gemini|Ollama|Offline/i)).toBeInTheDocument()
    })
  })
})
