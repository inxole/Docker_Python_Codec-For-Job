import React, { useState } from 'react'
import './App.css'

const Commpress_jpg_and_png = () => {
  // 複数ファイルを扱うための状態を配列として定義します
  const [files, setFiles] = useState<File[]>([])
  const [qualityRange, setQualityRange] = useState('40')
  const [uuidNumber, setUuidNumber] = useState("")

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const fileList = Array.from(event.target.files)
      const isValid = fileList.every(file =>
        file.name.toLowerCase().endsWith('.jpg') ||
        file.name.toLowerCase().endsWith('.jpeg') ||
        file.name.toLowerCase().endsWith('.png')
      )

      if (!isValid) {
        alert('jpgまたはpngのファイルのみアップロード可能です。')
        event.target.value = '' // ファイル選択をリセット
        return
      }

      setFiles(fileList)
    }
  }

  const handleQualityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQualityRange(event.target.value)
  }

  const uploadFiles = async () => {
    const quality = parseInt(qualityRange, 10)
    if (!files.length) {
      alert('ファイルを選択してください')
      return
    }
    if (isNaN(quality) || quality < 0 || quality > 100) {
      alert('圧縮の度合いは0から100の間で指定してください。')
      return
    }

    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    formData.append('quality_number', qualityRange)

    const response = await fetch('http://localhost:8000/upload_jpg_or_png/', {
      method: 'POST',
      body: formData,
    })

    if (response.status == 200) {
      const responseData = await response.json()
      if (responseData === null) {
        throw new Error('Some processing failed.')
      }
      setUuidNumber(responseData.message)
      alert('圧縮が完了しました。')
    } else if (response.status == 423) {
      alert(`ほかの人が使用中です。`)
    }
  }

  const downloadFile = async () => {
    if (uuidNumber === "") {
      alert('先にファイルをアップロードしてください。')
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/download-jpg-and-png/${uuidNumber}`);

      if (response.status === 200) {
        window.location.href = response.url
      } else if (response.status === 404) {
        alert('ファイルがまだ処理されていません。')
      } else {
        alert('何らかのエラーが発生しました。')
      }
    } catch (error) {
      console.error('Error fetching data: ', error)
      alert('サーバーに接続できませんでした。')
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 space-y-4" style={{ paddingTop: '200px' }}>
      <h1 className="text-3xl font-bold underline">JPG and PNG Compressor</h1>
      <input
        className="border-2 border-gray-300 p-2 rounded-md w-80"
        type="file"
        multiple
        onChange={handleFileChange}
      />
      <div>
        <label htmlFor="quality" className="block text-sm font-medium text-gray-700">圧縮の度合いを指定してください:</label>
        <div className="relative w-full">
          <input
            id="quality"
            accept=".jpg, .jpeg, .png"
            className="mt-1 block w-full pl-2 pr-8 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            type="text"
            placeholder="初期値：40"
            value={qualityRange}
            onChange={handleQualityChange}
          />
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            %
          </div>
        </div>
      </div>
      <button
        className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out"
        onClick={uploadFiles}
      >
        圧縮
      </button>
      <a href="#" onClick={downloadFile}>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">ダウンロード</button>
      </a>
    </div>
  )
}

export default Commpress_jpg_and_png
