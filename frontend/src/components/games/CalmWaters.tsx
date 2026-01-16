import { useEffect, useRef, useState } from 'react'

export function CalmWaters() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isPlaying, setIsPlaying] = useState(true)
  const animationRef = useRef<number>()

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = Math.min(canvas.offsetHeight, 500)
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Wave parameters
    let time = 0
    const waveAmplitude = 30
    const waveFrequency = 0.02
    const waveSpeed = 0.02

    const draw = () => {
      if (!isPlaying) return

      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw sky gradient
      const skyGradient = ctx.createLinearGradient(0, 0, 0, canvas.height / 2)
      skyGradient.addColorStop(0, '#87CEEB')
      skyGradient.addColorStop(1, '#E0F6FF')
      ctx.fillStyle = skyGradient
      ctx.fillRect(0, 0, canvas.width, canvas.height / 2)

      // Draw water
      ctx.fillStyle = '#4A90E2'
      ctx.beginPath()
      ctx.moveTo(0, canvas.height / 2)

      // Draw multiple wave layers
      for (let i = 0; i < 3; i++) {
        ctx.beginPath()
        ctx.moveTo(0, canvas.height / 2 + i * 20)

        for (let x = 0; x <= canvas.width; x += 5) {
          const y =
            canvas.height / 2 +
            i * 20 +
            Math.sin(x * waveFrequency + time + i) * (waveAmplitude - i * 5)
          ctx.lineTo(x, y)
        }

        ctx.lineTo(canvas.width, canvas.height)
        ctx.lineTo(0, canvas.height)
        ctx.closePath()

        const waterAlpha = 0.7 - i * 0.15
        ctx.fillStyle = `rgba(74, 144, 226, ${waterAlpha})`
        ctx.fill()
      }

      time += waveSpeed

      if (isPlaying) {
        animationRef.current = requestAnimationFrame(draw)
      }
    }

    if (isPlaying) {
      draw()
    }

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [isPlaying])

  return (
    <div className="w-full">
      <div className="mb-4 flex items-center justify-between">
        <p className="text-muted-foreground">
          Watch the peaceful waves and let your mind drift away...
        </p>
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>
      </div>
      <canvas
        ref={canvasRef}
        className="w-full h-[500px] rounded-lg border-2 border-primary/20 bg-gradient-to-b from-sky-200 to-blue-300"
        style={{ display: 'block' }}
      />
    </div>
  )
}
