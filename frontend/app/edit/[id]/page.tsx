'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core'
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable'
import { SortableItem } from '@/components/SortableItem'
import { PersonalDataForm } from '@/components/PersonalDataForm'
import { ExperienceForm } from '@/components/ExperienceForm'
import { EducationForm } from '@/components/EducationForm'
import { SkillsForm } from '@/components/SkillsForm'
import { Save, ArrowLeft, Download } from 'lucide-react'

interface CVData {
  personal: {
    name: string
    email: string
    phone: string
    address: string
    linkedin: string
    summary: string
  }
  experience: Array<{
    position: string
    company: string
    start_date: string
    end_date: string
    description: string
  }>
  education: Array<{
    degree: string
    institution: string
    start_date: string
    end_date: string
    description: string
  }>
  skills: string[]
  certifications: Array<{
    name: string
    issuer: string
    date: string
  }>
}

export default function EditPage({ params }: { params: { id: string } }) {
  const [cvData, setCvData] = useState<CVData | null>(null)
  const [company, setCompany] = useState<string>('galdora')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [activeTab, setActiveTab] = useState<'personal' | 'experience' | 'education' | 'skills'>('personal')
  const router = useRouter()

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  )

  useEffect(() => {
    // Load session data from localStorage
    const sessionData = localStorage.getItem('cvSession')
    if (sessionData) {
      const parsed = JSON.parse(sessionData)
      if (parsed.sessionId === params.id) {
        setCvData(parsed.extractedData)
        setCompany(parsed.company)
      }
    }
    setIsLoading(false)
  }, [params.id])

  const handleDragEnd = (event: any, type: 'experience' | 'education') => {
    const { active, over } = event

    if (active.id !== over.id) {
      setCvData((prev) => {
        if (!prev) return prev
        
        const oldIndex = prev[type].findIndex((item: any) => item.position === active.id)
        const newIndex = prev[type].findIndex((item: any) => item.position === over.id)
        
        return {
          ...prev,
          [type]: arrayMove(prev[type], oldIndex, newIndex)
        }
      })
    }
  }

  const updatePersonalData = (data: CVData['personal']) => {
    setCvData(prev => prev ? { ...prev, personal: data } : null)
  }

  const updateExperience = (data: CVData['experience']) => {
    setCvData(prev => prev ? { ...prev, experience: data } : null)
  }

  const updateEducation = (data: CVData['education']) => {
    setCvData(prev => prev ? { ...prev, education: data } : null)
  }

  const updateSkills = (data: string[]) => {
    setCvData(prev => prev ? { ...prev, skills: data } : null)
  }

  const saveData = async () => {
    if (!cvData) return
    
    setIsSaving(true)
    try {
      const response = await fetch(`http://localhost:8000/api/session/${params.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(cvData),
      })

      if (!response.ok) {
        throw new Error('Save failed')
      }

      // Update localStorage
      const sessionData = localStorage.getItem('cvSession')
      if (sessionData) {
        const parsed = JSON.parse(sessionData)
        parsed.extractedData = cvData
        localStorage.setItem('cvSession', JSON.stringify(parsed))
      }
    } catch (error) {
      console.error('Save error:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const exportToPDF = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/export/pdf/${params.id}`, {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error('Export failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `profile_${company}_${new Date().toISOString().split('T')[0]}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Export error:', error)
    }
  }

  const exportToDOCX = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/export/docx/${params.id}`, {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error('Export failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `profile_${company}_${new Date().toISOString().split('T')[0]}.docx`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Export error:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  if (!cvData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Session nicht gefunden</h1>
          <button
            onClick={() => router.push('/')}
            className="btn-primary"
          >
            Zurück zur Startseite
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/')}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-800"
              >
                <ArrowLeft className="h-5 w-5" />
                <span>Zurück</span>
              </button>
              <h1 className="text-2xl font-bold text-gray-800">Profil bearbeiten</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={saveData}
                disabled={isSaving}
                className="flex items-center space-x-2 btn-secondary"
              >
                <Save className="h-4 w-4" />
                <span>{isSaving ? 'Speichern...' : 'Speichern'}</span>
              </button>
              <button
                onClick={exportToPDF}
                className="flex items-center space-x-2 btn-primary"
              >
                <Download className="h-4 w-4" />
                <span>PDF Export</span>
              </button>
              <button
                onClick={exportToDOCX}
                className="flex items-center space-x-2 btn-primary"
              >
                <Download className="h-4 w-4" />
                <span>Word Export</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'personal', label: 'Persönlich', icon: '👤' },
              { id: 'experience', label: 'Berufserfahrung', icon: '💼' },
              { id: 'education', label: 'Ausbildung', icon: '🎓' },
              { id: 'skills', label: 'Fähigkeiten', icon: '🛠️' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-sm border">
          {activeTab === 'personal' && (
            <PersonalDataForm
              data={cvData.personal}
              onChange={updatePersonalData}
            />
          )}
          
          {activeTab === 'experience' && (
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={(event) => handleDragEnd(event, 'experience')}
            >
              <SortableContext
                items={cvData.experience.map(exp => exp.position)}
                strategy={verticalListSortingStrategy}
              >
                <ExperienceForm
                  data={cvData.experience}
                  onChange={updateExperience}
                />
              </SortableContext>
            </DndContext>
          )}
          
          {activeTab === 'education' && (
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={(event) => handleDragEnd(event, 'education')}
            >
              <SortableContext
                items={cvData.education.map(edu => edu.degree)}
                strategy={verticalListSortingStrategy}
              >
                <EducationForm
                  data={cvData.education}
                  onChange={updateEducation}
                />
              </SortableContext>
            </DndContext>
          )}
          
          {activeTab === 'skills' && (
            <SkillsForm
              data={cvData.skills}
              onChange={updateSkills}
            />
          )}
        </div>
      </main>
    </div>
  )
}
