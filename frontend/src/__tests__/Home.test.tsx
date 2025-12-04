import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href }: { children: React.ReactNode; href: string }) => {
    return <a href={href}>{children}</a>
  }
})

describe('Home Page', () => {
  it('renders the main heading', () => {
    render(<Home />)
    
    expect(screen.getByText(/Spotify Stats/i)).toBeInTheDocument()
  })

  it('renders the start button', () => {
    render(<Home />)
    
    expect(screen.getByText(/Rozpocznij/i)).toBeInTheDocument()
  })

  it('has a link to login page', () => {
    render(<Home />)
    
    const link = screen.getByRole('link', { name: /Rozpocznij/i })
    expect(link).toHaveAttribute('href', '/login')
  })
})
