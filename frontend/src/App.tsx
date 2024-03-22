import React, { useState } from 'react'
import './App.css'

const App = () => {
  const [file, setFile] = useState<File | null>(null)
  // ページ範囲を管理するための状態を追加します
  const [pageRange, setPageRange] = useState<string>('')

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  // ページ範囲のハンドラーを更新します
  const handlePageRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPageRange(event.target.value)
  }

  // ファイルアップロードの機能を更新します
  const uploadFile = () => {
    if (!file) {
      alert('ファイルを選択してください')
      return
    }

    // ページ範囲の形式を検証します
    const pageRangeRegex = /^(\d+(-\d+)?)(,\d+(-\d+)?)*$/
    if (!pageRangeRegex.test(pageRange)) {
      alert('ページ範囲が正しくありません。')
      return
    }

    const formData = new FormData();
    formData.append('pdf_file', file)
    // ページ範囲をフォームデータに追加します
    formData.append('pages', pageRange)

    fetch('http://localhost:8000/upload-pdf/', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data)
      })
      .catch(error => {
        console.error('Error:', error)
      })
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 space-y-4" style={{ paddingTop: '200px' }}>
      <h1 className="text-3xl font-bold underline">PDF to DXF Converter</h1>
      <input className="border-2 border-gray-300 p-2 rounded-md w-80" type="file" onChange={handleFileChange} />
      <div>
        <label htmlFor="pageRange" className="block text-sm font-medium text-gray-700">ページ範囲を指定:</label>
        <input
          id="pageRange"
          className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          type="text"
          placeholder="例：1, 3~10"
          value={pageRange}
          onChange={handlePageRangeChange}
        />
      </div>
      <button className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out" onClick={uploadFile}>変換</button>
      <a href='http://localhost:8000/download-dxf-zip/' target='_blank' rel='noopener noreferrer'>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">ダウンロード</button>
      </a>
    </div>
  )
}

export default App
