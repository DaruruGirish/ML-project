import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Alert, AlertDescription } from './ui/alert'
import { Twitter, User, Loader2, CheckCircle2, AlertCircle } from 'lucide-react'
import { MessageSquare } from 'lucide-react' // For Reddit icon
import { apiService } from '../lib/api'

interface AuthenticationSectionProps {
  isAuthenticated: boolean
  setIsAuthenticated: (value: boolean) => void
  isLoading: boolean
  setIsLoading: (value: boolean) => void
}

export function AuthenticationSection({
  isAuthenticated,
  setIsAuthenticated,
  isLoading,
  setIsLoading,
}: AuthenticationSectionProps) {
  const [username, setUsername] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const validateUsername = (value: string): boolean => {
    // Remove @ if present
    const cleanUsername = value.replace(/^@/, '')
    
    // Check length (Twitter usernames are 1-15 characters)
    if (cleanUsername.length < 1 || cleanUsername.length > 15) {
      setError('Username must be between 1 and 15 characters')
      return false
    }
    
    // Check for valid characters (alphanumeric and underscore only)
    if (!/^[a-zA-Z0-9_]+$/.test(cleanUsername)) {
      setError('Username can only contain letters, numbers, and underscores')
      return false
    }
    
    setError('')
    return true
  }

  const handleOAuth = async (platform: 'twitter' | 'reddit' = 'twitter') => {
    setIsLoading(true)
    setError('')
    setSuccess('')
    
    try {
      const authUrl = platform === 'reddit' 
        ? await apiService.getRedditAuthUrl()
        : await apiService.getTwitterAuthUrl()
      if (authUrl) {
        // Redirect to OAuth
        window.location.href = authUrl
      } else {
        throw new Error(`Failed to get ${platform} authorization URL`)
      }
    } catch (err: any) {
      setError(err.message || `Failed to initiate ${platform} authentication`)
      setIsLoading(false)
    }
  }

  const handleManualSubmit = async (e: React.FormEvent, platform: 'twitter' | 'reddit' = 'twitter') => {
    e.preventDefault()
    setError('')
    setSuccess('')
    
    if (!username.trim()) {
      setError('Please enter a username')
      return
    }
    
    if (platform === 'twitter' && !validateUsername(username)) {
      return
    }
    
    // Reddit username validation
    if (platform === 'reddit') {
      const cleanUsername = username.replace(/^u\//, '').replace(/\/u\//, '').trim()
      if (cleanUsername.length < 3 || cleanUsername.length > 20) {
        setError('Reddit username must be between 3 and 20 characters')
        return
      }
      if (!cleanUsername.replace('_', '').match(/^[a-zA-Z0-9_]+$/)) {
        setError('Reddit username can only contain letters, numbers, and underscores')
        return
      }
    }
    
    setIsLoading(true)
    
    try {
      const response = await apiService.manualAuth(username, platform)
      if (response.status === 'success') {
        setIsAuthenticated(true)
        const prefix = platform === 'twitter' ? '@' : 'u/'
        setSuccess(response.message || `Successfully connected to ${prefix}${username.replace(/^[@u\/]/, '')}`)
        // Trigger analysis after authentication
        handleAnalysis(username, platform)
      } else {
        throw new Error(response.message || 'Authentication failed')
      }
    } catch (err: any) {
      setError(err.message || `Failed to authenticate. Please check the ${platform} username and try again.`)
      setIsLoading(false)
    }
  }

  const handleAnalysis = async (usernameToAnalyze?: string, platform: 'twitter' | 'reddit' = 'twitter') => {
    try {
      setIsLoading(true)
      const response = await apiService.analyzeUser(usernameToAnalyze, platform)
      if (response.status === 'success') {
        setSuccess('Analysis completed successfully!')
        // Analysis results are now available
      } else {
        throw new Error(response.message || 'Analysis failed')
      }
    } catch (err: any) {
      setError(err.message || `Failed to analyze ${platform} content. Please try again.`)
    } finally {
      setIsLoading(false)
    }
  }

  // Check auth status on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await apiService.checkAuthStatus()
        if (response.status === 'authenticated') {
          setIsAuthenticated(true)
        }
      } catch (err) {
        // Not authenticated, continue
      }
    }
    checkAuth()
  }, [])

  if (isAuthenticated) {
    return (
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-2xl">
          <Alert variant="success" className="mb-6">
            <CheckCircle2 className="h-4 w-4" />
            <AlertDescription className="font-medium">
              {success || 'Successfully authenticated! Analysis dashboard will appear here.'}
            </AlertDescription>
          </Alert>
          <Card>
            <CardHeader>
              <CardTitle>Analysis Dashboard</CardTitle>
              <CardDescription>
                Your stress analysis results will appear here once processing is complete.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-center py-12">
                <div className="text-center space-y-4">
                  <Loader2 className="h-12 w-12 text-primary animate-spin mx-auto" />
                  <p className="text-muted-foreground">
                    Analyzing tweets and generating insights...
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    )
  }

  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-transparent to-accent/20">
      <div className="container mx-auto max-w-4xl">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Get Started</h2>
          <p className="text-muted-foreground text-lg">
            Connect your Twitter/X or Reddit account to analyze your posts for stress patterns
          </p>
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert variant="success" className="mb-6">
            <CheckCircle2 className="h-4 w-4" />
            <AlertDescription>{success}</AlertDescription>
          </Alert>
        )}

        <div className="space-y-8">
          {/* Twitter Section */}
          <div>
            <h3 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <Twitter className="h-5 w-5 text-primary" />
              <span>Twitter/X</span>
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              {/* Twitter OAuth Card */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary/50">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <Twitter className="h-5 w-5 text-primary" />
                    <CardTitle>Connect Twitter/X Account</CardTitle>
                  </div>
                  <CardDescription>
                    Securely authenticate with your Twitter/X account for full access
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    onClick={() => handleOAuth('twitter')}
                    disabled={isLoading}
                    className="w-full"
                    size="lg"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Connecting...
                      </>
                    ) : (
                      <>
                        <Twitter className="mr-2 h-4 w-4" />
                        Connect with Twitter/X
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>

              {/* Twitter Manual Entry Card */}
              <Card className="hover:shadow-lg transition-shadow border-2 hover:border-primary/30">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <User className="h-5 w-5 text-primary" />
                    <CardTitle>Manual Twitter/X Entry</CardTitle>
                  </div>
                  <CardDescription>
                    Enter a Twitter/X username to analyze public tweets
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={(e) => handleManualSubmit(e, 'twitter')} className="space-y-4">
                    <div>
                      <Input
                        type="text"
                        placeholder="Enter Twitter/X username (e.g., @username)"
                        value={username}
                        onChange={(e) => {
                          setUsername(e.target.value)
                          setError('')
                        }}
                        disabled={isLoading}
                        className="w-full"
                      />
                    </div>
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full"
                      size="lg"
                      variant="outline"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <User className="mr-2 h-4 w-4" />
                          Analyze Twitter Account
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Reddit Section */}
          <div>
            <h3 className="text-xl font-semibold mb-4 flex items-center space-x-2">
              <MessageSquare className="h-5 w-5 text-orange-500" />
              <span>Reddit</span>
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              {/* Reddit OAuth Card */}
              <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-orange-500/50">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <MessageSquare className="h-5 w-5 text-orange-500" />
                    <CardTitle>Connect Reddit Account</CardTitle>
                  </div>
                  <CardDescription>
                    Securely authenticate with your Reddit account to analyze your posts and comments
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    onClick={() => handleOAuth('reddit')}
                    disabled={isLoading}
                    className="w-full bg-orange-500 hover:bg-orange-600"
                    size="lg"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Connecting...
                      </>
                    ) : (
                      <>
                        <MessageSquare className="mr-2 h-4 w-4" />
                        Connect with Reddit
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>

              {/* Reddit Manual Entry Card */}
              <Card className="hover:shadow-lg transition-shadow border-2 hover:border-orange-500/30">
                <CardHeader>
                  <div className="flex items-center space-x-2 mb-2">
                    <User className="h-5 w-5 text-orange-500" />
                    <CardTitle>Manual Reddit Entry</CardTitle>
                  </div>
                  <CardDescription>
                    Enter a Reddit username to analyze public posts and comments
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={(e) => handleManualSubmit(e, 'reddit')} className="space-y-4">
                    <div>
                      <Input
                        type="text"
                        placeholder="Enter Reddit username (e.g., u/username)"
                        value={username}
                        onChange={(e) => {
                          setUsername(e.target.value)
                          setError('')
                        }}
                        disabled={isLoading}
                        className="w-full"
                      />
                    </div>
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full"
                      size="lg"
                      variant="outline"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <User className="mr-2 h-4 w-4" />
                          Analyze Reddit Account
                        </>
                      )}
                    </Button>
                  </form>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
