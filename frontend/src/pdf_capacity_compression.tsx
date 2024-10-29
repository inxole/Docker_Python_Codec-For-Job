import React, { useState } from 'react'
import './App.css'
import { TailSpin } from 'react-loader-spinner'

const Commpress_pdf = () => {
  const [file, setFile] = useState<File | null>(null)
  const [uuid_number, setUuid_Number] = useState("")
  const [loading, setLoading] = useState(false)
  const domain = import.meta.env.VITE_BACK_URL

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

  const uploadFile = async () => {
    if (!file) {
      alert('PDFファイルを選択してください')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('upload_pdf_for_converter', file)

    try {
      const response = await fetch(domain + '/pdf_for_compression/', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': domain
        },
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
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('ファイルのアップロード中にエラーが発生しました。')
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = async () => {
    if (uuid_number === "") {
      alert('先にファイルをアップロードしてください。')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(domain + `/download-pdf/${uuid_number}`, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': domain
        },
      })

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
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 space-y-4" style={{ paddingTop: '200px', position: 'relative' }}>
      <h1 className="text-3xl font-bold underline">PDF 圧縮</h1>
      <input className="border-2 border-gray-300 p-2 rounded-md w-80" type="file" onChange={handleFileChange} accept=".pdf" />

      <button
        className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out"
        onClick={uploadFile}
      >圧縮
      </button>

      <a href="#" onClick={downloadFile}>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">
          ダウンロード
        </button>
      </a>
      {loading && (
        <div style={
          {
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)', // 半透明の黒
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 10,
          }
        }>
          <TailSpin height={80} width={80} color="#ff8c00" ariaLabel="tail-spin-loading" />
        </div>
      )}
    </div>
  )
}

export default Commpress_pdf
