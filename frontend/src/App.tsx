import { useState } from 'react'
import { Header } from './components/Header'
import { Hero } from './components/Hero'
import { AuthenticationSection } from './components/AuthenticationSection'
import { FeaturesSection } from './components/FeaturesSection'
import { GamesSection } from './components/GamesSection'
import { BlogsSection } from './components/BlogsSection'
import { BlogDetail } from './components/BlogDetail'
import { Footer } from './components/Footer'

interface Resource {
  id: number
  title: string
  description: string
  resource_type: string
  category: string
  url: string
  source: string
  icon_name: string | null
  image_url: string | null
  read_time_minutes: number | null
  tags: string[]
  is_featured: boolean
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [selectedResourceId, setSelectedResourceId] = useState<number | null>(null)

  const handleResourceClick = (resource: Resource) => {
    setSelectedResourceId(resource.id)
    // Scroll to top when viewing a resource
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleBackToResources = () => {
    setSelectedResourceId(null)
    // Scroll to resources section
    setTimeout(() => {
      const resourcesSection = document.getElementById('resources')
      if (resourcesSection) {
        resourcesSection.scrollIntoView({ behavior: 'smooth' })
      }
    }, 100)
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        {selectedResourceId ? (
          <BlogDetail resourceId={selectedResourceId} onBack={handleBackToResources} />
        ) : (
          <>
            <Hero />
            <AuthenticationSection 
              isAuthenticated={isAuthenticated}
              setIsAuthenticated={setIsAuthenticated}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
            <FeaturesSection />
            <GamesSection />
            <BlogsSection onResourceClick={handleResourceClick} />
          </>
        )}
      </main>
      <Footer />
    </div>
  )
}

export default App
