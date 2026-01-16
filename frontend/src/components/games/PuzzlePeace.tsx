import { useEffect, useRef, useState, useCallback } from 'react'

interface Piece {
  x: number
  y: number
  correctX: number
  correctY: number
  image: HTMLImageElement | null
  sx: number
  sy: number
  sw: number
  sh: number
}

export function PuzzlePeace() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [pieces, setPieces] = useState<Piece[]>([])
  const [selectedPiece, setSelectedPiece] = useState<number | null>(null)
  const [solved, setSolved] = useState(false)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const cols = 3
    const rows = 3
    const pieceWidth = 200
    const pieceHeight = 150

    const resizeCanvas = () => {
      canvas.width = cols * pieceWidth
      canvas.height = rows * pieceHeight
    }
    resizeCanvas()

    // Create puzzle image (simple gradient pattern for demo)
    const createPuzzleImage = () => {
      const imgCanvas = document.createElement('canvas')
      imgCanvas.width = cols * pieceWidth
      imgCanvas.height = rows * pieceHeight
      const imgCtx = imgCanvas.getContext('2d')
      if (!imgCtx) return

      // Draw nature scene pattern
      const gradient = imgCtx.createLinearGradient(0, 0, 0, imgCanvas.height)
      gradient.addColorStop(0, '#87CEEB')
      gradient.addColorStop(0.5, '#90EE90')
      gradient.addColorStop(1, '#228B22')
      imgCtx.fillStyle = gradient
      imgCtx.fillRect(0, 0, imgCanvas.width, imgCanvas.height)

      // Add some decorative elements
      imgCtx.fillStyle = '#FFD700'
      for (let i = 0; i < 10; i++) {
        imgCtx.beginPath()
        imgCtx.arc(
          Math.random() * imgCanvas.width,
          Math.random() * imgCanvas.height,
          5,
          0,
          Math.PI * 2
        )
        imgCtx.fill()
      }

      return imgCanvas
    }

    const puzzleImage = createPuzzleImage()
    const newPieces: Piece[] = []

    // Create pieces
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const correctX = col * pieceWidth
        const correctY = row * pieceHeight
        const randomX = Math.random() * (canvas.width - pieceWidth)
        const randomY = Math.random() * (canvas.height - pieceHeight)

        newPieces.push({
          x: randomX,
          y: randomY,
          correctX,
          correctY,
          image: null,
          sx: correctX,
          sy: correctY,
          sw: pieceWidth,
          sh: pieceHeight,
        })
      }
    }

    // Shuffle pieces
    for (let i = newPieces.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[newPieces[i], newPieces[j]] = [newPieces[j], newPieces[i]]
    }

    if (pieces.length === 0) {
      setPieces(newPieces)
      return () => {}
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      pieces.forEach((piece, index) => {
        // Draw piece background
        ctx.fillStyle = index === selectedPiece ? '#FFE082' : '#F5F5F5'
        ctx.fillRect(piece.x, piece.y, pieceWidth, pieceHeight)
        ctx.strokeStyle = '#333'
        ctx.lineWidth = 2
        ctx.strokeRect(piece.x, piece.y, pieceWidth, pieceHeight)

        // Draw piece image
        if (puzzleImage) {
          ctx.drawImage(
            puzzleImage,
            piece.sx,
            piece.sy,
            piece.sw,
            piece.sh,
            piece.x,
            piece.y,
            pieceWidth,
            pieceHeight
          )
        }

        // Draw number
        ctx.fillStyle = '#000'
        ctx.font = '20px Arial'
        ctx.fillText(
          (index + 1).toString(),
          piece.x + 10,
          piece.y + 25
        )
      })

      // Check if solved
      const allCorrect = pieces.every((piece, index) => {
        const row = Math.floor(index / cols)
        const col = index % cols
        const correctX = col * pieceWidth
        const correctY = row * pieceHeight
        return (
          Math.abs(piece.x - correctX) < 10 &&
          Math.abs(piece.y - correctY) < 10
        )
      })

      if (allCorrect && !solved) {
        setSolved(true)
      }
    }

    draw()

    const handleClick = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      // Find clicked piece
      const clickedIndex = pieces.findIndex(
        (piece) =>
          x >= piece.x &&
          x <= piece.x + pieceWidth &&
          y >= piece.y &&
          y <= piece.y + pieceHeight
      )

      if (clickedIndex !== -1) {
        if (selectedPiece === clickedIndex) {
          setSelectedPiece(null)
        } else if (selectedPiece !== null) {
          // Swap pieces
          const updatedPieces = [...pieces]
          const temp = { ...updatedPieces[selectedPiece] }
          updatedPieces[selectedPiece] = { ...updatedPieces[clickedIndex] }
          updatedPieces[clickedIndex] = temp
          setPieces(updatedPieces)
          setSelectedPiece(null)
        } else {
          setSelectedPiece(clickedIndex)
        }
      }
    }

    canvas.addEventListener('click', handleClick)

    return () => {
      canvas.removeEventListener('click', handleClick)
    }
  }, [pieces, selectedPiece, solved])

  const resetPuzzle = () => {
    setSolved(false)
    setSelectedPiece(null)
    window.location.reload()
  }

  return (
    <div className="w-full">
      <div className="mb-4 space-y-2">
        <p className="text-muted-foreground">
          Click two pieces to swap them. Arrange all pieces correctly to solve the puzzle.
        </p>
        {solved && (
          <div className="p-4 bg-green-100 rounded-lg text-green-800 font-semibold">
            🎉 Puzzle solved! Great job!
          </div>
        )}
        <button
          onClick={resetPuzzle}
          className="px-4 py-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
        >
          Reset Puzzle
        </button>
      </div>
      <canvas
        ref={canvasRef}
        className="w-full rounded-lg border-2 border-primary/20 bg-white mx-auto"
        style={{ display: 'block', maxWidth: '600px' }}
      />
    </div>
  )
}
