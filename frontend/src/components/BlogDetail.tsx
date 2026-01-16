import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { ArrowLeft, ExternalLink, Clock, Tag } from 'lucide-react'
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

export function BlogDetail({ resourceId, onBack }: { resourceId: number; onBack: () => void }) {
  const [resource, setResource] = useState<Resource | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadResource()
  }, [resourceId])

  const loadResource = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await apiService.getResource(resourceId)
      if (response.status === 'success' && response.resource) {
        setResource(response.resource)
      } else {
        setError('Resource not found')
      }
    } catch (err) {
      console.error('Error loading resource:', err)
      setError('Failed to load resource')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center">
            <p className="text-muted-foreground">Loading...</p>
          </div>
        </div>
      </div>
    )
  }

  if (error || !resource) {
    return (
      <div className="min-h-screen py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
        <div className="container mx-auto max-w-4xl">
          <Card>
            <CardContent className="pt-6">
              <p className="text-destructive">{error || 'Resource not found'}</p>
              <Button onClick={onBack} className="mt-4" variant="outline">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back to Resources
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto max-w-4xl">
        <Button 
          onClick={onBack} 
          variant="ghost" 
          className="mb-6"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Resources
        </Button>

        <Card className="overflow-hidden">
          {resource.image_url && (
            <div className="w-full h-64 sm:h-96 overflow-hidden bg-muted">
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

          <CardHeader className="space-y-4">
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <CardTitle className="text-3xl sm:text-4xl mb-2">{resource.title}</CardTitle>
                {resource.source && (
                  <p className="text-lg text-primary font-medium">{resource.source}</p>
                )}
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
              {resource.read_time_minutes && (
                <div className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  <span>{resource.read_time_minutes} min read</span>
                </div>
              )}
              {resource.category && (
                <div className="flex items-center gap-1">
                  <Tag className="h-4 w-4" />
                  <span className="capitalize">{resource.category}</span>
                </div>
              )}
            </div>

            {resource.tags && resource.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 pt-2">
                {resource.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 text-sm font-medium rounded-full bg-primary/10 text-primary"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </CardHeader>

          <CardContent className="space-y-6">
            <CardDescription className="text-lg leading-relaxed">
              {resource.description}
            </CardDescription>

            <div className="pt-4 border-t">
              <p className="text-sm text-muted-foreground mb-4">
                To read the full article, click the link below to visit the source website.
              </p>
              <Button
                onClick={() => window.open(resource.url, '_blank', 'noopener,noreferrer')}
                className="w-full sm:w-auto"
              >
                Read Full Article
                <ExternalLink className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
