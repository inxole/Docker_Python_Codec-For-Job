import React, { useState } from 'react'
import './App.css'

const Commpress_pdf = () => {
  const [file, setFile] = useState<File | null>(null)
  const [uuid_number, setUuid_Number] = useState("")

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedFile = event.target.files[0]
      if (selectedFile.type !== 'application/pdf') {
        alert('PDFファイルのみ選択してください。')
        setFile(null)  // ファイル選択をリセット
      } else {
        setFile(selectedFile)
      }
    }
  }

  // ファイルアップロードの機能を更新します
  const uploadFile = async () => {
    if (!file) {
      alert('PDFファイルを選択してください')
      return
    }

    const formData = new FormData()
    formData.append('upload_pdf_for_converter', file)

    const response = await fetch('http://localhost:8000/pdf_for_compression/', {
      method: 'POST',
      body: formData,
    })

    if (response.status === 200) {
      const responce_data = await response.json()
      if (responce_data === null) {
        throw new Error('Some processing failed.')
      }
      setUuid_Number(responce_data.message)
      alert('圧縮が完了しました。')
    } else if (response.status === 423) {
      alert('他の人が利用中です。')
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 space-y-4" style={{ paddingTop: '200px' }}>
      <h1 className="text-3xl font-bold underline">PDF Compressor</h1>
      <input className="border-2 border-gray-300 p-2 rounded-md w-80" type="file" onChange={handleFileChange} accept=".pdf" />
      <button className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out" onClick={uploadFile}>圧縮</button>
      <a href={`http://localhost:8000/download-pdf/${uuid_number}`} target='_blank' rel='noopener noreferrer'>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">ダウンロード</button>
      </a>
    </div>
  )
}

export default Commpress_pdf
