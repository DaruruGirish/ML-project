import { useEffect, useRef, useState } from 'react'

export function BreathingBubble() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isBreathing, setIsBreathing] = useState(true)
  const [phase, setPhase] = useState<'inhale' | 'hold' | 'exhale'>('inhale')
  const [breathCount, setBreathCount] = useState(0)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = Math.min(canvas.offsetHeight, 500)
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    let size = 50
    let targetSize = 150
    let animationSpeed = 0.02
    let currentPhase: 'inhale' | 'hold' | 'exhale' = 'inhale'
    let phaseTime = 0
    let count = 0

    const phases = {
      inhale: { duration: 4000, target: 150 },
      hold: { duration: 2000, target: 150 },
      exhale: { duration: 6000, target: 50 },
    }

    const draw = () => {
      if (!isBreathing) return

      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw background gradient
      const gradient = ctx.createRadialGradient(
        canvas.width / 2,
        canvas.height / 2,
        0,
        canvas.width / 2,
        canvas.height / 2,
        Math.max(canvas.width, canvas.height)
      )
      gradient.addColorStop(0, '#E8F5E9')
      gradient.addColorStop(1, '#C8E6C9')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Update phase
      phaseTime += 16 // ~60fps
      const currentPhaseConfig = phases[currentPhase]

      if (phaseTime >= currentPhaseConfig.duration) {
        phaseTime = 0
        if (currentPhase === 'inhale') {
          currentPhase = 'hold'
          setPhase('hold')
        } else if (currentPhase === 'hold') {
          currentPhase = 'exhale'
          setPhase('exhale')
        } else {
          currentPhase = 'inhale'
          setPhase('inhale')
          count++
          setBreathCount(count)
        }
      }

      // Animate size
      const target = phases[currentPhase].target
      size += (target - size) * animationSpeed

      // Draw bubble
      const x = canvas.width / 2
      const y = canvas.height / 2

      // Outer glow
      const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, size + 20)
      glowGradient.addColorStop(0, 'rgba(76, 175, 80, 0.3)')
      glowGradient.addColorStop(1, 'rgba(76, 175, 80, 0)')
      ctx.fillStyle = glowGradient
      ctx.beginPath()
      ctx.arc(x, y, size + 20, 0, Math.PI * 2)
      ctx.fill()

      // Main bubble
      const bubbleGradient = ctx.createRadialGradient(
        x - size * 0.3,
        y - size * 0.3,
        0,
        x,
        y,
        size
      )
      bubbleGradient.addColorStop(0, 'rgba(129, 199, 132, 0.9)')
      bubbleGradient.addColorStop(1, 'rgba(76, 175, 80, 0.7)')
      ctx.fillStyle = bubbleGradient
      ctx.beginPath()
      ctx.arc(x, y, size, 0, Math.PI * 2)
      ctx.fill()

      // Highlight
      ctx.fillStyle = 'rgba(255, 255, 255, 0.4)'
      ctx.beginPath()
      ctx.arc(x - size * 0.3, y - size * 0.3, size * 0.3, 0, Math.PI * 2)
      ctx.fill()

      requestAnimationFrame(draw)
    }

    if (isBreathing) {
      draw()
    }

    return () => {
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [isBreathing])

  const getInstruction = () => {
    switch (phase) {
      case 'inhale':
        return 'Breathe in slowly...'
      case 'hold':
        return 'Hold...'
      case 'exhale':
        return 'Breathe out slowly...'
    }
  }

  return (
    <div className="w-full">
      <div className="mb-4 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-bold mb-2">{getInstruction()}</h3>
            <p className="text-muted-foreground">
              Follow the bubble as it expands and contracts. Breathe with it.
            </p>
          </div>
          <button
            onClick={() => setIsBreathing(!isBreathing)}
            className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
          >
            {isBreathing ? 'Pause' : 'Resume'}
          </button>
        </div>
        <div className="text-center">
          <p className="text-lg font-semibold">Breath Count: {breathCount}</p>
        </div>
      </div>
      <canvas
        ref={canvasRef}
        className="w-full h-[500px] rounded-lg border-2 border-primary/20 bg-gradient-to-br from-green-50 to-green-100"
        style={{ display: 'block' }}
      />
    </div>
  )
}
