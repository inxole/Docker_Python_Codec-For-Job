import { useState } from 'react'
import './App.css'

const Converter_dxf = () => {
  const [file, setFile] = useState<File | null>()
  // ページ範囲を管理するための状態を追加します
  const [pageRange, setPageRange] = useState('')
  const [uuid_number, setUuid_Number] = useState("")
  const domain = import.meta.env.VITE_BACK_URL

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
  const uploadFile = async () => {
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

    const formData = new FormData()
    formData.append('upload_pdf_file', file)
    // ページ範囲をフォームデータに追加します
    formData.append('pages', pageRange)

    const response = await fetch(domain + '/upload-pdf/', {
      method: 'POST',
      body: formData,
      headers: {
        'Access-Control-Allow-Origin': domain
      },
    })

    if (response.status == 200) {
      const responce_data = await response.json()
      if (responce_data === null) {
        throw new Error('Some processing failed.')
      }
      setUuid_Number(responce_data.message)
      alert('変換が完了しました。')
    } else if (response.status == 423) {
      alert('他の人が利用中です。')
    }
  }

  const downloadFile = async () => {
    if (uuid_number === "") {
      alert('先にファイルをアップロードしてください。')
      return
    }

    try {
      const response = await fetch(domain + `/download-dxf-zip/${uuid_number}`, {
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
    }
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
      <a href="#" onClick={downloadFile}>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">ダウンロード</button>
      </a>
      <p className="text-lg px-4 py-2 text-red-500">※現在、ベクター形式のPDFファイルしか変換できません。</p>
    </div>
  )
}

export default Converter_dxf
