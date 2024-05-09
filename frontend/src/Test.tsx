import React, { useState, useEffect } from 'react'

interface Opinion {
  id: string
  content: string
}

const App: React.FC = () => {
  const [opinions, setOpinions] = useState<Opinion[]>([])
  const [content, setContent] = useState('')

  useEffect(() => {
    fetch('http://localhost:8000/opinions/')
      .then(response => response.json())
      .then(data => setOpinions(data))
  }, [])

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    const newOpinion = { id: String(Math.random()), content }
    const response = await fetch('http://localhost:8000/opinions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newOpinion),
    })
    const result = await response.json()
    setOpinions([result, ...opinions])
    setContent('')
  }

  const handleDelete = async (opinionId: string) => {
    const response = await fetch(`http://localhost:8000/opinions/${opinionId}`, {
      method: 'DELETE',
    })
    if (response.ok) {
      setOpinions(opinions.filter((opinion) => opinion.id !== opinionId))
    }
  }

  return (
    <div className="flex flex-col items-center justify-start min-h-screen bg-gray-100 pt-10">
      <h2 className="text-xl font-bold mb-4">ご意見・ご要望</h2>
      <p className="text-lg px-4 py-2">例１：自動的にスケジュールを管理するソフトウェアが欲しいです。</p>
      <p className="text-lg px-4 py-2">例２：「使用方法」を各プログラムに作成してください。</p>
      <p className="text-lg px-4 py-2">例３：「DXF変換」が使いにくいです。</p>
      <form onSubmit={handleSubmit} className="w-full max-w-lg">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="w-full p-4 text-lg border rounded shadow resize-none"
          placeholder="Your opinion here..."
          rows={3}
        />
        <button type="submit" className="mt-4 px-4 py-2 bg-blue-500 text-white rounded shadow">
          登録
        </button>
      </form>
      <div className="mt-4 w-full max-w-lg">
        {opinions.map((opinion) => (
          <div key={opinion.id} className="p-4 mb-2 bg-white rounded shadow flex justify-between items-center">
            <span>{opinion.content}</span>
            <button
              onClick={() => handleDelete(opinion.id)}
              className="ml-4 px-4 py-2 bg-red-500 text-white rounded shadow"
            >
              削除
            </button>
          </div>
        ))}
      </div>
    </div>
  )

}

export default App

