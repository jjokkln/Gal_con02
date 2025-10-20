'use client'

import { useState, useEffect } from 'react'
import { Plus, X } from 'lucide-react'

interface SkillsFormProps {
  data: string[]
  onChange: (data: string[]) => void
}

export function SkillsForm({ data, onChange }: SkillsFormProps) {
  const [skills, setSkills] = useState<string[]>(data)
  const [newSkill, setNewSkill] = useState('')

  useEffect(() => {
    setSkills(data)
  }, [data])

  const addSkill = () => {
    if (newSkill.trim() && !skills.includes(newSkill.trim())) {
      const newSkills = [...skills, newSkill.trim()]
      setSkills(newSkills)
      onChange(newSkills)
      setNewSkill('')
    }
  }

  const removeSkill = (index: number) => {
    const newSkills = skills.filter((_, i) => i !== index)
    setSkills(newSkills)
    onChange(newSkills)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      addSkill()
    }
  }

  return (
    <div className="p-6">
      <h2 className="section-header">Fähigkeiten & Kompetenzen</h2>
      
      {/* Add new skill */}
      <div className="flex space-x-2 mb-6">
        <input
          type="text"
          value={newSkill}
          onChange={(e) => setNewSkill(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Neue Fähigkeit hinzufügen..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <button
          onClick={addSkill}
          className="flex items-center space-x-2 btn-primary"
        >
          <Plus className="h-4 w-4" />
          <span>Hinzufügen</span>
        </button>
      </div>

      {/* Skills list */}
      {skills.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>Noch keine Fähigkeiten hinzugefügt.</p>
          <p className="text-sm">Füge deine Fähigkeiten und Kompetenzen hinzu.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {skills.map((skill, index) => (
            <div
              key={index}
              className="flex items-center justify-between bg-gray-50 border border-gray-200 rounded-lg px-4 py-2"
            >
              <span className="text-gray-800">{skill}</span>
              <button
                onClick={() => removeSkill(index)}
                className="text-red-500 hover:text-red-700 p-1"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Bulk import */}
      <div className="mt-8">
        <h3 className="text-lg font-medium text-gray-800 mb-3">Fähigkeiten importieren</h3>
        <p className="text-sm text-gray-600 mb-3">
          Du kannst mehrere Fähigkeiten auf einmal hinzufügen, indem du sie durch Kommas trennst:
        </p>
        <textarea
          placeholder="JavaScript, React, Python, Machine Learning, Projektmanagement..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          rows={3}
          onChange={(e) => {
            const bulkSkills = e.target.value
              .split(',')
              .map(skill => skill.trim())
              .filter(skill => skill && !skills.includes(skill))
            
            if (bulkSkills.length > 0) {
              const newSkills = [...skills, ...bulkSkills]
              setSkills(newSkills)
              onChange(newSkills)
              e.target.value = ''
            }
          }}
        />
      </div>
    </div>
  )
}
