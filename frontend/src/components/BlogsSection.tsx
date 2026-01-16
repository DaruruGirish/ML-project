import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { BookOpen, Globe, Gamepad2, MoreHorizontal, Clock, ExternalLink, Brain, Leaf, Heart, Sparkles, Waves, Activity, Headphones, PenTool, Wind } from 'lucide-react'
import apiService from '../lib/api'

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

const iconMap: { [key: string]: any } = {
  Brain,
  Leaf,
  Heart,
  Sparkles,
  BookOpen,
  Globe,
  Gamepad2,
  Waves,
  Activity,
  Headphones,
  PenTool,
  Wind,
}

export function BlogsSection({ onResourceClick }: { onResourceClick: (resource: Resource) => void }) {
  const [resources, setResources] = useState<Resource[]>([])
  const [filteredResources, setFilteredResources] = useState<Resource[]>([])
  const [activeFilter, setActiveFilter] = useState<string>('blog')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadResources()
  }, [])

  useEffect(() => {
    filterResources()
  }, [activeFilter, resources])

  const loadResources = async () => {
    try {
      setLoading(true)
      const response = await apiService.getResources()
      if (response.status === 'success' && response.resources) {
        setResources(response.resources)
      }
    } catch (error) {
      console.error('Error loading resources:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterResources = () => {
    if (activeFilter === 'blog') {
      setFilteredResources(resources.filter(r => r.resource_type === 'blog'))
    } else if (activeFilter === 'wikipedia') {
      setFilteredResources(resources.filter(r => r.resource_type === 'wikipedia'))
    } else if (activeFilter === 'game') {
      setFilteredResources(resources.filter(r => r.resource_type === 'game'))
    } else {
      setFilteredResources(resources)
    }
  }

  const getIcon = (iconName: string | null) => {
    if (!iconName) return BookOpen
    return iconMap[iconName] || BookOpen
  }

  const filters = [
    { id: 'blog', label: 'Blogs', icon: BookOpen },
    { id: 'wikipedia', label: 'Wikipedia', icon: Globe },
    { id: 'game', label: 'Games', icon: Gamepad2 },
    { id: 'more', label: '+ More', icon: MoreHorizontal },
  ]

  if (loading) {
    return (
      <section id="resources" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center">
            <p className="text-muted-foreground">Loading resources...</p>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section id="resources" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">Find Your Path to Calm</h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            Discover curated resources to help manage stress and improve your mental well-being. From educational content to interactive experiences, we have got you covered.
          </p>
        </div>

        {/* Filter Navigation */}
        <div className="flex justify-center mb-8">
          <div className="inline-flex rounded-lg bg-muted p-1">
            {filters.map((filter) => {
              const Icon = filter.icon
              const isActive = activeFilter === filter.id
              return (
                <button
                  key={filter.id}
                  onClick={() => setActiveFilter(filter.id)}
                  className={`
                    px-4 py-2 rounded-md flex items-center gap-2 transition-all
                    ${isActive 
                      ? 'bg-background text-foreground shadow-sm' 
                      : 'text-muted-foreground hover:text-foreground'
                    }
                  `}
                >
                  <Icon className="h-4 w-4" />
                  <span className="text-sm font-medium">{filter.label}</span>
                </button>
              )
            })}
          </div>
        </div>

        {/* Resources Grid */}
        <div className="grid md:grid-cols-2 gap-6">
          {filteredResources.length === 0 ? (
            <div className="col-span-2 text-center py-12">
              <p className="text-muted-foreground">No resources found in this category.</p>
            </div>
          ) : (
            filteredResources.map((resource) => {
              const Icon = getIcon(resource.icon_name)
              return (
                <Card 
                  key={resource.id} 
                  className={`hover:shadow-lg transition-all duration-300 hover:-translate-y-1 overflow-hidden ${
                    resource.resource_type === 'wikipedia' 
                      ? 'border-2 hover:border-teal-500/30' 
                      : 'border-2 hover:border-primary/30'
                  }`}
                >
                  <div className="relative">
                    {resource.image_url && (
                      <div className="w-full h-48 overflow-hidden bg-muted">
                        <img 
                          src={resource.image_url} 
                          alt={resource.title}
                          className="w-full h-full object-cover"
                          onError={(e) => {
                            (e.target as HTMLImageElement).style.display = 'none'
                          }}
                        />
                      </div>
                    )}
                    <div className="absolute top-4 left-4">
                      <div className={`p-2 rounded-lg backdrop-blur-sm ${
                        resource.resource_type === 'wikipedia' 
                          ? 'bg-teal-500/20' 
                          : 'bg-background/90'
                      }`}>
                        <Icon className={`h-5 w-5 ${
                          resource.resource_type === 'wikipedia' 
                            ? 'text-teal-600 dark:text-teal-400' 
                            : 'text-primary'
                        }`} />
                      </div>
                    </div>
                    {resource.read_time_minutes && (
                      <div className="absolute top-4 right-4">
                        <div className="px-3 py-1 rounded-full bg-background/90 backdrop-blur-sm flex items-center gap-1">
                          <Clock className="h-3 w-3 text-muted-foreground" />
                          <span className="text-xs font-medium text-muted-foreground">
                            {resource.read_time_minutes} min read
                          </span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <CardHeader>
                    <CardTitle className="text-xl">{resource.title}</CardTitle>
                    {resource.resource_type === 'wikipedia' ? (
                      <p className="text-sm text-muted-foreground font-medium">Wikipedia Article</p>
                    ) : resource.source && (
                      <p className="text-sm text-primary font-medium">{resource.source}</p>
                    )}
                  </CardHeader>
                  
                  <CardContent>
                    <CardDescription className="text-base leading-relaxed mb-4">
                      {resource.description}
                    </CardDescription>
                    
                    {resource.tags && resource.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {resource.tags.map((tag, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 text-xs font-medium rounded-full bg-primary/10 text-primary"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    <div className="flex items-center justify-between">
                      {resource.resource_type === 'wikipedia' ? (
                        <Button
                          variant="outline"
                          className="w-full"
                          onClick={() => window.open(resource.url, '_blank', 'noopener,noreferrer')}
                        >
                          Read on Wikipedia
                          <ExternalLink className="ml-2 h-4 w-4" />
                        </Button>
                      ) : (
                        <Button
                          variant="ghost"
                          className="text-primary hover:text-primary/80 p-0 h-auto font-medium"
                          onClick={() => onResourceClick(resource)}
                        >
                          Read
                          <ExternalLink className="ml-2 h-4 w-4" />
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>

        {/* Wikipedia Footer Disclaimer */}
        {activeFilter === 'wikipedia' && filteredResources.length > 0 && (
          <div className="mt-8 text-center">
            <p className="text-sm text-muted-foreground">
              Content sourced from Wikipedia, the free encyclopedia.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}
