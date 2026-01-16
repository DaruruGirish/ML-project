import { useState } from 'react'

interface Sound {
  id: string
  name: string
  icon: string
  playing: boolean
  volume: number
}

export function SoundScape() {
  const [sounds, setSounds] = useState<Sound[]>([
    { id: 'rain', name: 'Rain', icon: '🌧️', playing: false, volume: 50 },
    { id: 'forest', name: 'Forest', icon: '🌲', playing: false, volume: 50 },
    { id: 'ocean', name: 'Ocean', icon: '🌊', playing: false, volume: 50 },
    { id: 'fire', name: 'Fireplace', icon: '🔥', playing: false, volume: 50 },
    { id: 'wind', name: 'Wind', icon: '💨', playing: false, volume: 50 },
    { id: 'birds', name: 'Birds', icon: '🐦', playing: false, volume: 50 },
  ])

  // Note: In a real implementation, you would use Web Audio API or pre-recorded audio files
  // For this demo, we'll simulate the audio controls
  const toggleSound = (id: string) => {
    setSounds((prevSounds) =>
      prevSounds.map((sound) =>
        sound.id === id ? { ...sound, playing: !sound.playing } : sound
      )
    )

    // In a real app, you would play/pause actual audio here
    // const audio = audioRefs.current[id]
    // if (audio) {
    //   if (playing) {
    //     audio.pause()
    //   } else {
    //     audio.play()
    //   }
    // }
  }

  const updateVolume = (id: string, volume: number) => {
    setSounds((prevSounds) =>
      prevSounds.map((sound) =>
        sound.id === id ? { ...sound, volume } : sound
      )
    )

    // In a real app, you would update audio volume here
    // const audio = audioRefs.current[id]
    // if (audio) {
    //   audio.volume = volume / 100
    // }
  }

  const playingSounds = sounds.filter((s) => s.playing).length

  return (
    <div className="w-full">
      <div className="mb-6 space-y-4">
        <div>
          <h3 className="text-2xl font-bold mb-2">Ambient Sound Mixer</h3>
          <p className="text-muted-foreground">
            Mix your own peaceful soundscape. Toggle sounds on/off and adjust volumes to create the perfect relaxing atmosphere.
          </p>
          {playingSounds > 0 && (
            <p className="mt-2 text-sm font-semibold text-primary">
              {playingSounds} sound{playingSounds !== 1 ? 's' : ''} playing
            </p>
          )}
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sounds.map((sound) => (
          <div
            key={sound.id}
            className={`p-6 rounded-lg border-2 transition-all ${
              sound.playing
                ? 'bg-primary/10 border-primary shadow-lg'
                : 'bg-muted border-muted-foreground/20'
            }`}
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className="text-4xl">{sound.icon}</span>
                <div>
                  <h4 className="font-semibold text-lg">{sound.name}</h4>
                  <p className="text-sm text-muted-foreground">
                    {sound.playing ? 'Playing' : 'Stopped'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => toggleSound(sound.id)}
                className={`px-4 py-2 rounded-md font-medium transition-colors ${
                  sound.playing
                    ? 'bg-red-500 text-white hover:bg-red-600'
                    : 'bg-green-500 text-white hover:bg-green-600'
                }`}
              >
                {sound.playing ? 'Stop' : 'Play'}
              </button>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-muted-foreground">
                Volume: {sound.volume}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={sound.volume}
                onChange={(e) => updateVolume(sound.id, parseInt(e.target.value))}
                className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer accent-primary"
              />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> This is a demo interface. In a full implementation, actual ambient audio would play using the Web Audio API or pre-loaded audio files. 
          You can integrate services like <a href="https://freesound.org" target="_blank" rel="noopener noreferrer" className="underline">Freesound</a> or use your own audio assets.
        </p>
      </div>
    </div>
  )
}
