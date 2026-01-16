import { Sparkles } from 'lucide-react'

export function Hero() {
  return (
    <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-secondary/5 to-accent/5" />
      <div className="container mx-auto relative z-10">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center justify-center mb-6">
            <Sparkles className="h-8 w-8 text-primary animate-pulse" />
          </div>
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent">
            Understand Your Digital Wellbeing
          </h2>
          <p className="text-xl text-muted-foreground mb-8 leading-relaxed">
            Analyze Twitter activity to understand stress patterns and gain insights into your mental health through language analysis.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <div className="px-4 py-2 rounded-full bg-primary/10 text-primary font-medium">
              🔒 Privacy-Focused
            </div>
            <div className="px-4 py-2 rounded-full bg-secondary/10 text-secondary font-medium">
              ⚡ Real-Time Analysis
            </div>
            <div className="px-4 py-2 rounded-full bg-accent/10 text-accent-foreground font-medium">
              📊 Data Visualization
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
