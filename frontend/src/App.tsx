import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Commpress_jpg_and_png from './jpg_and_png_capacity_compression'
import Commpress_pdf from './pdf_capacity_compression'
import Converter_dxf from './converter_pdf_to_dxf'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/compress-jpg-png" element={<Commpress_jpg_and_png />} />
        <Route path="/compress-pdf" element={<Commpress_pdf />} />
        <Route path="/convert-to-dxf" element={<Converter_dxf />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

function Home() {
  return (
    <div className="grid grid-cols-2 gap-4 p-8 justify-items-center">
      <Link to="/compress-jpg-png" className="bg-blue-500 text-white p-4 w-72 h-72 rounded-lg text-center justify-self-end">
        <img src="src/icon_image/icon_jpg_and_png_compressor.png" alt="JPG and PNG Compression" className="w-48 h-48 mx-auto mb-4" />
        <p>JPG & PNG 圧縮</p>
      </Link>
      <Link to="/compress-pdf" className="bg-green-500 text-white p-4 w-72 rounded-lg text-center justify-self-start">
        <img src="src/icon_image/icon_pdf_compressor.png" alt="PDF Compression" className="w-48 h-48 mx-auto mb-4" />
        <p>PDF 圧縮</p>
      </Link>
      <Link to="/convert-to-dxf" className="bg-yellow-500 text-white p-4 w-72 rounded-lg text-center justify-self-end">
        <img src="src/icon_image/icon_pdf_to_dxf_converter.png" alt="Convert to DXF" className="w-48 h-48 mx-auto mb-4" />
        <p>DXF 変換</p>
      </Link>
    </div>
  )
}
