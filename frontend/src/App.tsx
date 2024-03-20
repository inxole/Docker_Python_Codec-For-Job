import React, { useState } from 'react'

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null)
  const [pages, setPages] = useState<number>(1)

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0])
    }
  }

  const handlePagesChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPages(parseInt(event.target.value))
  }

  const uploadFile = () => {
    if (!file) {
      alert('Please select a file')
      return
    }

    const formData = new FormData();
    formData.append('pdf_file', file)
    formData.append('pages', pages.toString())

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

  const downloadFile = () => {
    fetch('http://localhost:8000/download_dxf.zip/', {
      method: 'GET',
    })
      .then(response => response.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'dxf_files.zip'
        document.body.appendChild(a)
        a.click()
        a.remove()
      })
      .catch(error => {
        console.error('Error:', error)
      });
  };

  return (
    <div>
      <h1>PDF to DXF Converter</h1>
      <input type="file" onChange={handleFileChange} />
      <input type="number" value={pages} onChange={handlePagesChange} />
      <button onClick={uploadFile}>Upload PDF</button>
      <button onClick={downloadFile}>Download DXF</button>
      <a href='http://localhost:8000/download-dxf-zip/' target='_blank' rel='noopener noreferrer'>link</a>
    </div>
  )
}

export default App
