import { useEffect, useRef, useState } from 'react'

export function ZenGarden() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [stones, setStones] = useState<Array<{ x: number; y: number; size: number }>>([])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = Math.min(canvas.offsetHeight, 500)
      drawGarden()
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    const drawGarden = () => {
      // Draw sand background
      ctx.fillStyle = '#F5E6D3'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw sand texture
      ctx.fillStyle = '#E8D5B7'
      for (let i = 0; i < 1000; i++) {
        const x = Math.random() * canvas.width
        const y = Math.random() * canvas.height
        ctx.fillRect(x, y, 1, 1)
      }

      // Draw rake lines
      ctx.strokeStyle = '#D4C4A8'
      ctx.lineWidth = 1
      for (let i = 0; i < 20; i++) {
        ctx.beginPath()
        ctx.moveTo(i * (canvas.width / 20), 0)
        ctx.lineTo(i * (canvas.width / 20), canvas.height)
        ctx.stroke()
      }

      // Draw stones
      stones.forEach((stone) => {
        ctx.fillStyle = '#8B7D6B'
        ctx.beginPath()
        ctx.arc(stone.x, stone.y, stone.size, 0, Math.PI * 2)
        ctx.fill()
        ctx.strokeStyle = '#6B5D4B'
        ctx.lineWidth = 2
        ctx.stroke()
      })
    }

    drawGarden()

    let lastX = 0
    let lastY = 0

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDrawing) return

      const rect = canvas.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      ctx.strokeStyle = '#D4C4A8'
      ctx.lineWidth = 3
      ctx.lineCap = 'round'
      ctx.beginPath()
      ctx.moveTo(lastX, lastY)
      ctx.lineTo(x, y)
      ctx.stroke()

      lastX = x
      lastY = y
    }

    const handleMouseDown = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      lastX = e.clientX - rect.left
      lastY = e.clientY - rect.top
      setIsDrawing(true)
    }

    const handleMouseUp = () => {
      setIsDrawing(false)
    }

    const handleClick = (e: MouseEvent) => {
      if (e.shiftKey) {
        const rect = canvas.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top
        const size = Math.random() * 15 + 10
        setStones([...stones, { x, y, size }])
        drawGarden()
      }
    }

    canvas.addEventListener('mousedown', handleMouseDown)
    canvas.addEventListener('mousemove', handleMouseMove)
    canvas.addEventListener('mouseup', handleMouseUp)
    canvas.addEventListener('click', handleClick)

    return () => {
      window.removeEventListener('resize', resizeCanvas)
      canvas.removeEventListener('mousedown', handleMouseDown)
      canvas.removeEventListener('mousemove', handleMouseMove)
      canvas.removeEventListener('mouseup', handleMouseUp)
      canvas.removeEventListener('click', handleClick)
    }
  }, [isDrawing, stones])

  const clearGarden = () => {
    setStones([])
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    ctx.fillStyle = '#F5E6D3'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
  }

  return (
    <div className="w-full">
      <div className="mb-4 space-y-2">
        <p className="text-muted-foreground">
          Drag to create patterns in the sand. Shift + Click to place stones. Create your peaceful zen garden.
        </p>
        <button
          onClick={clearGarden}
          className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Clear Garden
        </button>
      </div>
      <canvas
        ref={canvasRef}
        className="w-full h-[500px] rounded-lg border-2 border-primary/20 cursor-crosshair bg-[#F5E6D3]"
        style={{ display: 'block' }}
      />
    </div>
  )
}
