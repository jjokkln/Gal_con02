'use client'

import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const [company, setCompany] = useState<'galdora' | 'bejob'>('galdora')
  const [isUploading, setIsUploading] = useState(false)
  const [uploadError, setUploadError] = useState<string | null>(null)
  const router = useRouter()

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]
    setIsUploading(true)
    setUploadError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('company', company)

      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Upload failed')
      }

      const result = await response.json()
      
      // Store session data in localStorage
      localStorage.setItem('cvSession', JSON.stringify({
        sessionId: result.session_id,
        company: result.company,
        extractedData: result.extracted_data
      }))

      // Redirect to edit page
      router.push(`/edit/${result.session_id}`)
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : 'Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false
  })

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="text-center py-12">
        <h1 className="text-6xl font-bold text-gray-800 mb-4">
          📄 CV2Profile
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Konvertiere deinen Lebenslauf in eine professionelle Profilvorlage mit KI-Unterstützung
        </p>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-4">
        <div className="w-full max-w-4xl">
          {/* Company Selection */}
          <div className="glass-card p-8 mb-8">
            <h2 className="text-2xl font-semibold text-white mb-6 text-center">
              Unternehmen auswählen
            </h2>
            <div className="flex justify-center space-x-8">
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name="company"
                  value="galdora"
                  checked={company === 'galdora'}
                  onChange={(e) => setCompany(e.target.value as 'galdora')}
                  className="w-5 h-5 text-primary-600"
                />
                <span className="text-white font-medium">Galdora</span>
              </label>
              <label className="flex items-center space-x-3 cursor-pointer">
                <input
                  type="radio"
                  name="company"
                  value="bejob"
                  checked={company === 'bejob'}
                  onChange={(e) => setCompany(e.target.value as 'bejob')}
                  className="w-5 h-5 text-primary-600"
                />
                <span className="text-white font-medium">BeJob</span>
              </label>
            </div>
          </div>

          {/* Upload Area */}
          <div className="glass-card p-12">
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200 ${
                isDragActive
                  ? 'border-primary-400 bg-primary-50/20'
                  : 'border-white/30 hover:border-white/50 hover:bg-white/5'
              }`}
            >
              <input {...getInputProps()} />
              
              <div className="flex flex-col items-center space-y-4">
                {isUploading ? (
                  <>
                    <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
                    <p className="text-white text-lg">Analysiere Lebenslauf...</p>
                  </>
                ) : (
                  <>
                    <Upload className="h-16 w-16 text-white/70" />
                    <div>
                      <p className="text-white text-xl font-medium mb-2">
                        {isDragActive
                          ? 'Datei hier ablegen'
                          : 'Lebenslauf hier ablegen oder klicken zum Auswählen'
                        }
                      </p>
                      <p className="text-white/70">
                        Unterstützte Formate: PDF, DOCX, JPG, PNG (max. 10MB)
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Error Message */}
            {uploadError && (
              <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg flex items-center space-x-2">
                <AlertCircle className="h-5 w-5 text-red-400" />
                <span className="text-red-200">{uploadError}</span>
              </div>
            )}
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mt-12">
            <div className="glass-card-dark p-6 text-center">
              <FileText className="h-12 w-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">KI-Extraktion</h3>
              <p className="text-white/70 text-sm">
                Automatische Extraktion aller relevanten Daten aus deinem Lebenslauf
              </p>
            </div>
            <div className="glass-card-dark p-6 text-center">
              <CheckCircle className="h-12 w-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Professionelle Templates</h3>
              <p className="text-white/70 text-sm">
                Angepasst an dein Unternehmen mit modernem Design
              </p>
            </div>
            <div className="glass-card-dark p-6 text-center">
              <Upload className="h-12 w-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Einfacher Export</h3>
              <p className="text-white/70 text-sm">
                Download als PDF oder Word-Dokument
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center py-8 text-gray-600">
        <p>&copy; 2024 CV2Profile. Alle Rechte vorbehalten.</p>
      </footer>
    </div>
  )
}
