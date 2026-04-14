import { render, screen } from '@testing-library/react'
import MessageBubble from '../MessageBubble'

describe('MessageBubble', () => {
  it('renders user message content', () => {
    render(
      <MessageBubble
        message={{ role: 'user', content: 'What is AC-2?' }}
      />
    )
    expect(screen.getByText('What is AC-2?')).toBeInTheDocument()
  })

  it('renders assistant message with agent name', () => {
    render(
      <MessageBubble
        message={{
          role: 'assistant',
          content: 'AC-2 is Account Management.',
          agent_name: 'NIST Controls Specialist',
        }}
      />
    )
    expect(screen.getByText('NIST Controls Specialist')).toBeInTheDocument()
  })

  it('renders sources section when sources provided', () => {
    render(
      <MessageBubble
        message={{
          role: 'assistant',
          content: 'Answer text.',
          sources: [
            { source: 'nist_80053r5.pdf', page: 42, content_snippet: 'AC-2...' },
          ],
        }}
      />
    )
    expect(screen.getByText(/Sources/i)).toBeInTheDocument()
  })

  it('renders markdown bold as strong element', () => {
    const { container } = render(
      <MessageBubble
        message={{ role: 'assistant', content: '**AC-2** is important.' }}
      />
    )
    const strong = container.querySelector('strong')
    expect(strong).toBeInTheDocument()
    expect(strong?.textContent).toBe('AC-2')
  })

  it('shows copy button for assistant messages', () => {
    render(
      <MessageBubble
        message={{ role: 'assistant', content: 'Some answer.' }}
      />
    )
    // The copy button uses a Copy icon from lucide-react
    const buttons = screen.getAllByRole('button')
    expect(buttons.length).toBeGreaterThan(0)
  })
})
