'use client'

import { useState, useEffect } from 'react'
import { SortableItem } from './SortableItem'
import { Plus, Trash2 } from 'lucide-react'

interface EducationItem {
  degree: string
  institution: string
  start_date: string
  end_date: string
  description: string
}

interface EducationFormProps {
  data: EducationItem[]
  onChange: (data: EducationItem[]) => void
}

export function EducationForm({ data, onChange }: EducationFormProps) {
  const [education, setEducation] = useState<EducationItem[]>(data)

  useEffect(() => {
    setEducation(data)
  }, [data])

  const handleChange = (index: number, field: keyof EducationItem, value: string) => {
    const newEducation = [...education]
    newEducation[index] = { ...newEducation[index], [field]: value }
    setEducation(newEducation)
    onChange(newEducation)
  }

  const addEducation = () => {
    const newEducation = [...education, {
      degree: '',
      institution: '',
      start_date: '',
      end_date: '',
      description: ''
    }]
    setEducation(newEducation)
    onChange(newEducation)
  }

  const removeEducation = (index: number) => {
    const newEducation = education.filter((_, i) => i !== index)
    setEducation(newEducation)
    onChange(newEducation)
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="section-header">Ausbildung & Weiterbildung</h2>
        <button
          onClick={addEducation}
          className="flex items-center space-x-2 btn-primary"
        >
          <Plus className="h-4 w-4" />
          <span>Hinzufügen</span>
        </button>
      </div>

      {education.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>Noch keine Ausbildung hinzugefügt.</p>
          <p className="text-sm">Klicke auf "Hinzufügen" um eine neue Ausbildung hinzuzufügen.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {education.map((edu, index) => (
            <SortableItem key={`${edu.degree}-${index}`} id={edu.degree || `edu-${index}`}>
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-medium text-gray-800">
                  {edu.degree || 'Neuer Abschluss'} - {edu.institution || 'Neue Institution'}
                </h3>
                <button
                  onClick={() => removeEducation(index)}
                  className="text-red-500 hover:text-red-700 p-1"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Abschluss *
                  </label>
                  <input
                    type="text"
                    value={edu.degree}
                    onChange={(e) => handleChange(index, 'degree', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Bachelor of Science Informatik"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Institution *
                  </label>
                  <input
                    type="text"
                    value={edu.institution}
                    onChange={(e) => handleChange(index, 'institution', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Technische Universität München"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Startdatum
                  </label>
                  <input
                    type="text"
                    value={edu.start_date}
                    onChange={(e) => handleChange(index, 'start_date', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="10/2018"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Enddatum
                  </label>
                  <input
                    type="text"
                    value={edu.end_date}
                    onChange={(e) => handleChange(index, 'end_date', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="09/2022"
                  />
                </div>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Beschreibung
                </label>
                <textarea
                  value={edu.description}
                  onChange={(e) => handleChange(index, 'description', e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Zusätzliche Informationen wie Schwerpunkte, Noten, Projekte..."
                />
              </div>
            </SortableItem>
          ))}
        </div>
      )}
    </div>
  )
}
