'use client'

import { useState, useEffect } from 'react'
import { SortableItem } from './SortableItem'
import { Plus, Trash2 } from 'lucide-react'

interface ExperienceItem {
  position: string
  company: string
  start_date: string
  end_date: string
  description: string
}

interface ExperienceFormProps {
  data: ExperienceItem[]
  onChange: (data: ExperienceItem[]) => void
}

export function ExperienceForm({ data, onChange }: ExperienceFormProps) {
  const [experience, setExperience] = useState<ExperienceItem[]>(data)

  useEffect(() => {
    setExperience(data)
  }, [data])

  const handleChange = (index: number, field: keyof ExperienceItem, value: string) => {
    const newExperience = [...experience]
    newExperience[index] = { ...newExperience[index], [field]: value }
    setExperience(newExperience)
    onChange(newExperience)
  }

  const addExperience = () => {
    const newExperience = [...experience, {
      position: '',
      company: '',
      start_date: '',
      end_date: '',
      description: ''
    }]
    setExperience(newExperience)
    onChange(newExperience)
  }

  const removeExperience = (index: number) => {
    const newExperience = experience.filter((_, i) => i !== index)
    setExperience(newExperience)
    onChange(newExperience)
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="section-header">Berufserfahrung</h2>
        <button
          onClick={addExperience}
          className="flex items-center space-x-2 btn-primary"
        >
          <Plus className="h-4 w-4" />
          <span>Hinzufügen</span>
        </button>
      </div>

      {experience.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>Noch keine Berufserfahrung hinzugefügt.</p>
          <p className="text-sm">Klicke auf "Hinzufügen" um eine neue Position hinzuzufügen.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {experience.map((exp, index) => (
            <SortableItem key={`${exp.position}-${index}`} id={exp.position || `exp-${index}`}>
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-medium text-gray-800">
                  {exp.position || 'Neue Position'} bei {exp.company || 'Neues Unternehmen'}
                </h3>
                <button
                  onClick={() => removeExperience(index)}
                  className="text-red-500 hover:text-red-700 p-1"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Position *
                  </label>
                  <input
                    type="text"
                    value={exp.position}
                    onChange={(e) => handleChange(index, 'position', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Softwareentwickler"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Unternehmen *
                  </label>
                  <input
                    type="text"
                    value={exp.company}
                    onChange={(e) => handleChange(index, 'company', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="Muster GmbH"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Startdatum
                  </label>
                  <input
                    type="text"
                    value={exp.start_date}
                    onChange={(e) => handleChange(index, 'start_date', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="01/2020"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Enddatum
                  </label>
                  <input
                    type="text"
                    value={exp.end_date}
                    onChange={(e) => handleChange(index, 'end_date', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    placeholder="12/2023 oder Present"
                  />
                </div>
              </div>

              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Beschreibung
                </label>
                <textarea
                  value={exp.description}
                  onChange={(e) => handleChange(index, 'description', e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Beschreibe deine Aufgaben und Erfolge in dieser Position..."
                />
              </div>
            </SortableItem>
          ))}
        </div>
      )}
    </div>
  )
}
