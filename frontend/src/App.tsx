import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Commpress_jpg_and_png from './jpg_and_png_capacity_compression'
import Commpress_pdf from './pdf_capacity_compression'
import Converter_dxf from './converter_pdf_to_dxf'
import SplitOrTiePDF from './pdf_split_or_tie'
import Cutout_Video from './flv_cutout'
import OpinionForm from './opinion'
import jpg_and_png_compressor_icon from './icon_image/icon_jpg_and_png_compressor.png'
import PdfCompressorIcon from './icon_image/icon_pdf_compressor.png'
import dxfConverterIcon from './icon_image/icon_pdf_to_dxf_converter.png'
import splitOrTieIcon from './icon_image/split_or_tie_pdf.png'
import videoCutoutIcon from './icon_image/flv_cutout.png'

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/compress-jpg-png" element={<Commpress_jpg_and_png />} />
        <Route path="/compress-pdf" element={<Commpress_pdf />} />
        <Route path="/convert-to-dxf" element={<Converter_dxf />} />
        <Route path="/pdf-split-or-tie" element={<SplitOrTiePDF />} />
        <Route path="/cutout-video" element={<Cutout_Video />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

function Home() {
  return (
    <div>
      <div className="grid grid-cols-2 gap-4 p-8 justify-items-center">
        <Link to="/compress-jpg-png" className="bg-blue-500 text-white p-4 w-72 h-72 rounded-lg text-center justify-self-end">
          <img src={jpg_and_png_compressor_icon} alt="JPG and PNG Compression" className="w-48 h-48 mx-auto mb-4" />
          <p>JPG & PNG 圧縮</p>
        </Link>
        <Link to="/compress-pdf" className="bg-green-500 text-white p-4 w-72 rounded-lg text-center justify-self-start">
          <img src={PdfCompressorIcon} alt="PDF Compression" className="w-48 h-48 mx-auto mb-4" />
          <p>PDF 圧縮</p>
        </Link>
        <Link to="/convert-to-dxf" className="bg-yellow-500 text-white p-4 w-72 h-72 rounded-lg text-center justify-self-end">
          <img src={dxfConverterIcon} alt="Convert to DXF" className="w-48 h-48 mx-auto mb-4" />
          <p>DXF 変換</p>
        </Link>
        <Link to="/pdf-split-or-tie" className="bg-red-500 text-white p-4 w-72 rounded-lg text-center justify-self-start">
                    <img src={splitOrTieIcon} alt="PDF Split ot Tie" className="w-48 h-48 mx-auto mb-4" style={{ transform: 'scale(2, 1.3)' }} />
          <p>PDF 分割・結合</p>
        </Link>
        <Link to="/cutout-video" className="bg-purple-500 text-white p-4 w-72 h-72 rounded-lg text-center justify-self-end">
          <img src={videoCutoutIcon} alt="Cutout Video" className="w-48 h-48 mx-auto mb-4" />
          <p>動画切り抜き</p>
        </Link>
      </div>
      <div>
        <OpinionForm />
      </div>
    </div>
  )
}
