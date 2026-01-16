import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Waves, Leaf, Heart, Sparkles, Puzzle, Headphones, Star, Play, X } from 'lucide-react'
import { CalmWaters } from './games/CalmWaters'
import { ZenGarden } from './games/ZenGarden'
import { BreathingBubble } from './games/BreathingBubble'
import { ColorFlow } from './games/ColorFlow'
import { PuzzlePeace } from './games/PuzzlePeace'
import { SoundScape } from './games/SoundScape'

interface Game {
  id: string
  title: string
  category: string
  description: string
  icon: any
  color: string
  isFeatured: boolean
}

const featuredGames: Game[] = [
  {
    id: 'calm-waters',
    title: 'Calm Waters',
    category: 'Relaxation',
    description: 'Peaceful ocean simulation with soothing sounds. Just watch the waves and relax.',
    icon: Waves,
    color: 'text-blue-500',
    isFeatured: true,
  },
  {
    id: 'zen-garden',
    title: 'Zen Garden',
    category: 'Creative',
    description: 'Create and maintain your own virtual zen garden with sand patterns and stones.',
    icon: Leaf,
    color: 'text-green-500',
    isFeatured: true,
  },
  {
    id: 'breathing-bubble',
    title: 'Breathing Bubble',
    category: 'Breathing',
    description: 'Follow the expanding and contracting bubble to practice deep breathing exercises.',
    icon: Heart,
    color: 'text-pink-500',
    isFeatured: true,
  },
]

const moreGames: Game[] = [
  {
    id: 'color-flow',
    title: 'Color Flow',
    category: 'Visual',
    description: 'Relaxing color mixing game with gentle animations and ambient sounds.',
    icon: Sparkles,
    color: 'text-purple-500',
    isFeatured: false,
  },
  {
    id: 'puzzle-peace',
    title: 'Puzzle Peace',
    category: 'Puzzle',
    description: 'Simple, calming jigsaw puzzles with nature scenes and soft music.',
    icon: Puzzle,
    color: 'text-amber-600',
    isFeatured: false,
  },
  {
    id: 'soundscape',
    title: 'SoundScape',
    category: 'Audio',
    description: 'Mix your own ambient soundscape with rain, forest, and nature sounds.',
    icon: Headphones,
    color: 'text-emerald-500',
    isFeatured: false,
  },
]

const GameModal = ({ game, onClose }: { game: Game | null; onClose: () => void }) => {
  if (!game) return null

  const renderGame = () => {
    switch (game.id) {
      case 'calm-waters':
        return <CalmWaters />
      case 'zen-garden':
        return <ZenGarden />
      case 'breathing-bubble':
        return <BreathingBubble />
      case 'color-flow':
        return <ColorFlow />
      case 'puzzle-peace':
        return <PuzzlePeace />
      case 'soundscape':
        return <SoundScape />
      default:
        return <div>Game not found</div>
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div className="relative bg-background rounded-lg shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-2xl font-bold">{game.title}</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="rounded-full"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
        <div className="p-4 overflow-auto max-h-[calc(90vh-80px)]">
          {renderGame()}
        </div>
      </div>
    </div>
  )
}

export function GamesSection() {
  const [selectedGame, setSelectedGame] = useState<Game | null>(null)

  const renderGameCard = (game: Game, isFeatured: boolean) => {
    const Icon = game.icon
    return (
      <Card
        key={game.id}
        className="hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/30"
      >
        <CardHeader>
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-lg bg-gradient-to-br ${game.color.replace('text-', 'from-')}/20 ${game.color.replace('text-', 'to-')}/5 w-fit`}>
              <Icon className={`h-6 w-6 ${game.color}`} />
            </div>
            {isFeatured && (
              <div className="flex items-center gap-1 text-yellow-500">
                <Star className="h-4 w-4 fill-yellow-500" />
              </div>
            )}
          </div>
          <div className="flex items-center gap-2 mb-2">
            <CardTitle className="text-xl">{game.title}</CardTitle>
          </div>
          <span className="inline-block px-2 py-1 text-xs font-medium rounded-full bg-muted text-muted-foreground">
            {game.category}
          </span>
        </CardHeader>
        <CardContent>
          <CardDescription className="text-base leading-relaxed mb-4">
            {game.description}
          </CardDescription>
          <Button
            onClick={() => setSelectedGame(game)}
            className={isFeatured ? 'w-full bg-primary hover:bg-primary/90' : 'w-full bg-muted hover:bg-muted/80 text-foreground'}
          >
            {isFeatured ? (
              <>
                <Play className="mr-2 h-4 w-4" />
                Play Now
              </>
            ) : (
              'Play'
            )}
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <>
      <section id="games" className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-muted/20 to-background">
        <div className="container mx-auto max-w-6xl">
          {/* Featured Games Section */}
          <div className="mb-16">
            <div className="flex items-center gap-2 mb-8">
              <Star className="h-6 w-6 text-yellow-500 fill-yellow-500" />
              <h2 className="text-3xl sm:text-4xl font-bold">Featured Games</h2>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featuredGames.map((game) => renderGameCard(game, true))}
            </div>
          </div>

          {/* More Games Section */}
          <div className="mb-8">
            <h2 className="text-3xl sm:text-4xl font-bold mb-8">More Games</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {moreGames.map((game) => renderGameCard(game, false))}
            </div>
          </div>

          {/* Game API Integration Info */}
          <div className="mt-12 p-6 rounded-lg bg-gradient-to-br from-green-50 to-green-100/50 border-2 border-green-200/50">
            <div className="flex items-start gap-4">
              <div className="p-3 rounded-lg bg-green-500/20">
                <Headphones className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold mb-2 text-green-900">Built-in Relaxation Games</h3>
                <p className="text-green-800">
                  All games are built directly into the platform using HTML5 Canvas and Web Audio APIs. 
                  No external dependencies required - just pure, calming experiences designed to help you relax and unwind.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Game Modal */}
      {selectedGame && (
        <GameModal game={selectedGame} onClose={() => setSelectedGame(null)} />
      )}
    </>
  )
}
