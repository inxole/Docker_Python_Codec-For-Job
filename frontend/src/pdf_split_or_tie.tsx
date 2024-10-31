import React, { useState } from 'react'
import './App.css'
import { TailSpin } from 'react-loader-spinner'

const SplitOrTiePDF = () => {
  const [splitFile, setSplitFile] = useState<File | null>(null)
  const [tieFile, setTieFile] = useState<File[]>([])
  const [uuidNumber, setUuidNumber] = useState('')
  const [loading, setLoading] = useState(false)
  const [pageRange, setPageRange] = useState('')
  const domain = import.meta.env.VITE_BACK_URL

  // ページ範囲のハンドラーを更新します
  const handlePageRangeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPageRange(event.target.value)
  }

  const handleSplitFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedFile = event.target.files[0]
      if (selectedFile.type !== 'application/pdf') {
        alert('PDFファイルのみ選択してください。')
        setSplitFile(null)
      } else {
        setSplitFile(selectedFile)
      }
    }
  }

  const handleTieFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const fileList = Array.from(event.target.files)
      const isValid = fileList.every(file =>
        file.name.toLowerCase().endsWith('.pdf') ||
        file.name.toUpperCase().endsWith('.PDF')
      )
      if (!isValid) {
        alert('PDFファイルのみ選択してください。')
        event.target.value = ''
        return
      } else {
        setTieFile(fileList)
      }
    }
  }

  const uploadSplitFile = async () => {
    if (!splitFile) {
      alert('PDFファイルを選択してください')
      return
    }

    // ページ範囲の形式を検証します
    const pageRangeRegex = /^(\d+(-\d+)?)(,\d+(-\d+)?)*$/
    if (!pageRangeRegex.test(pageRange)) {
      alert('ページ範囲が正しくありません。')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('upload_pdf_for_split', splitFile)
    formData.append('pages', pageRange)

    try {
      const response = await fetch(domain + '/upload-pdf-split/', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': domain,
        },
      })

      if (response.status === 200) {
        const responseData = await response.json()
        if (responseData === null) {
          throw new Error('Some processing failed.')
        }
        setUuidNumber(responseData.message)
        alert('分割が完了しました。')
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

  const uploadTieFile = async () => {
    if (!tieFile) {
      alert('PDFファイルを選択してください')
      return
    }

    setLoading(true)
    const formData = new FormData()
    tieFile.forEach(file => {
      formData.append('files', file)
    })

    try {
      const response = await fetch(domain + '/upload-pdf-tie/', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': domain,
        },
      })

      if (response.status === 200) {
        const responseData = await response.json()
        if (responseData === null) {
          throw new Error('Some processing failed.')
        }
        setUuidNumber(responseData.message)
        alert('結合が完了しました。')
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
    if (uuidNumber === '') {
      alert('先にファイルをアップロードしてください。')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(domain + `/download-pdf-SoT-zip/${uuidNumber}`, {
        method: 'GET',
        headers: {
          'Access-Control-Allow-Origin': domain,
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
      <h1 className="text-3xl font-bold underline">PDF 分割・結合</h1>

      <div className="flex space-x-8">
        <div className="border-2 border-gray-300 rounded-md p-4">
          <h2 className="text-xl font-bold">PDF 分割</h2>
          <div className="flex flex-col items-center">
            <input className="border-2 border-gray-300 p-2 rounded-md w-80" type="file" onChange={handleSplitFileChange} accept=".pdf" />

            <div>
              <label htmlFor="pageRange" className="block text-sm font-medium text-gray-700">ページ範囲を指定</label>
              <input
                id="pageRange"
                className="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                type="text"
                placeholder="例：1, 3~10"
                value={pageRange}
                onChange={handlePageRangeChange}
              />
            </div>

            <button
              className="w-24 px-4 py-2 mt-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out"
              onClick={uploadSplitFile}
            >分割</button>
          </div>
        </div>

        <div className="border-2 border-gray-300 rounded-md p-4">
          <h2 className="text-xl font-bold">PDF 結合</h2>
          <div className="flex flex-col items-center">
            <input className="border-2 border-gray-300 p-2 rounded-md w-80" multiple type="file" onChange={handleTieFileChange} accept=".pdf" />
            <button
              className="w-24 px-4 py-2 mt-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out"
              onClick={uploadTieFile}
            >結合</button>
          </div>
        </div>
      </div>

      <a href="#" onClick={downloadFile}>
        <button className="px-4 py-2 mt-4 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">
          ダウンロード
        </button>
      </a>


      {loading && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 10,
        }}>
          <TailSpin height={80} width={80} color="#ff8c00" ariaLabel="tail-spin-loading" />
        </div>
      )}
    </div>
  )
}

export default SplitOrTiePDF
