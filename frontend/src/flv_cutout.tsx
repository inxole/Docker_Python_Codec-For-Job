import React, { useState } from 'react'
import './App.css'
import { TailSpin } from 'react-loader-spinner'

const Cutout_Video = () => {
  const [hours, setHours] = useState<number>(0)
  const [minutes, setMinutes] = useState<number>(0)
  const [seconds, setSeconds] = useState<number>(0)
  const [file, setFile] = useState<File | null>(null)
  const [uuidNumber, setUuidNumber] = useState("")
  const [loading, setLoading] = useState(false)
  const domain = import.meta.env.VITE_BACK_URL

  const handleHoursChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setHours(Number(event.target.value))
  }
  const handleMinutesChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setMinutes(Number(event.target.value))
  }
  const handleSecondsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSeconds(Number(event.target.value))
  }

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedFile = event.target.files[0]
      const fileExtension = selectedFile.name.split('.').pop()?.toLowerCase()
      if (fileExtension !== 'flv') {
        alert('FLVファイルのみ選択してください。')
        setFile(null)
      } else {
        setFile(selectedFile)
      }
    }
  }

  const uploadFile = async () => {
    if (!file) {
      alert('動画ファイルを選択してください')
      return
    }

    setLoading(true)
    const totalSeconds = hours * 3600 + minutes * 60 + seconds
    const formData = new FormData()
    formData.append('flv_file', file)
    formData.append('seconds', totalSeconds.toString())

    try {
      const response = await fetch(domain + '/upload-flv/', {
        method: 'POST',
        body: formData,
        headers: {
          'Access-Control-Allow-Origin': domain
        },
      })

      if (response.status === 200) {
        const responseData = await response.json()
        if (responseData === null) {
          throw new Error('処理が失敗しました。')
        }
        setUuidNumber(responseData.message)
        alert('切り抜きが完了しました。')
      } else if (response.status === 423) {
        alert('他のユーザーが利用中です。')
      }
    } catch (error) {
      console.error('ファイルのアップロード中にエラーが発生しました:', error)
      alert('ファイルのアップロード中にエラーが発生しました。')
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = async () => {
    if (uuidNumber === "") {
      alert('先にファイルをアップロードしてください。')
      return
    }

    setLoading(true)
    try {
      const response = await fetch(domain + `/download-flv-zip/${uuidNumber}`, {
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
      console.error('データ取得中にエラーが発生しました:', error)
      alert('サーバーに接続できませんでした。')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center pt-20 space-y-4" style={{ paddingTop: '200px', position: 'relative' }}>
      <h1 className="text-3xl font-bold underline">動画切り抜き</h1>
      <input className="border-2 border-gray-300 p-2 rounded-md w-80" type="file" onChange={handleFileChange} accept=".flv" />
      <div className="flex space-x-2">
        <input
          type="number"
          placeholder="時"
          value={hours}
          onChange={handleHoursChange}
          max={100}
          min={0}
          className="border-2 border-gray-300 p-2 rounded-md w-24"
        />
        <p className="flex items-center justify-center">時</p>
        <input
          type="number"
          placeholder="分"
          value={minutes}
          onChange={handleMinutesChange}
          min={0}
          max={59}
          className="border-2 border-gray-300 p-2 rounded-md w-24"
        />
        <p className="flex items-center justify-center">分</p>
        <input
          type="number"
          placeholder="秒"
          value={seconds}
          onChange={handleSecondsChange}
          min={0}
          max={59}
          className="border-2 border-gray-300 p-2 rounded-md w-24"
        />
        <p className="flex items-center justify-center">秒</p>
      </div>

      <button
        className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700 transition duration-200 ease-in-out"
        onClick={uploadFile}
      >切り抜き
      </button>

      <a href="#" onClick={downloadFile}>
        <button className="px-4 py-2 bg-green-500 text-white rounded shadow hover:bg-green-700 transition duration-200 ease-in-out">
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

export default Cutout_Video
