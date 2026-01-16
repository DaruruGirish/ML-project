import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Shield, Zap, BarChart3, UserCheck } from 'lucide-react'

export function FeaturesSection() {
  const features = [
    {
      icon: Shield,
      title: 'Privacy-Focused Analysis',
      description: 'Your data is processed securely and never stored permanently. We respect your privacy and only analyze what you authorize.',
      color: 'text-primary'
    },
    {
      icon: Zap,
      title: 'Real-Time Tweet Analysis',
      description: 'Get instant insights from recent Twitter activity. Our AI analyzes language patterns to detect stress indicators in real-time.',
      color: 'text-secondary'
    },
    {
      icon: BarChart3,
      title: 'Stress Pattern Visualization',
      description: 'Coming soon: Beautiful charts and graphs showing stress patterns over time, helping you understand trends in your digital wellbeing.',
      color: 'text-primary'
    },
    {
      icon: UserCheck,
      title: 'User Control Over Data',
      description: 'You have complete control. Disconnect anytime, choose what to analyze, and decide how your data is used.',
      color: 'text-secondary'
    },
  ]

  return (
    <section id="features" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">Why Choose Detect The Stress?</h2>
          <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
            A comprehensive tool designed with your mental health and privacy in mind
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Card key={index} className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/30">
                <CardHeader>
                  <div className={`p-3 rounded-lg bg-gradient-to-br ${feature.color === 'text-primary' ? 'from-primary/20 to-primary/5' : 'from-secondary/20 to-secondary/5'} w-fit mb-4`}>
                    <Icon className={`h-6 w-6 ${feature.color}`} />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>
    </section>
  )
}
