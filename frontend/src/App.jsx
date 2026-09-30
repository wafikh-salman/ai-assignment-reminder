import { useState } from 'react'
import './App.css'

function App() {
  const [assignment, setAssignment] = useState("")
  const [due_date, setDate] = useState("")
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState(null)
  const [dashboardData, setDashboardData] = useState(null)

  const getTodayString = () => {
    const now = new Date()
    const year = now.getFullYear()
    const month = String(now.getMonth() + 1).padStart(2, '0')
    const day = String(now.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }

  const handleAssignmentChange = (e) => {
    const value = e.target.value
    setAssignment(value)
    if (apiError) setApiError(null)
    if (errors.assignment && value.trim()) {
      setErrors((prev) => ({ ...prev, assignment: "" }))
    }
  }

  const handleDateChange = (e) => {
    const value = e.target.value
    setDate(value)
    if (apiError) setApiError(null)
    if (errors.due_date && value) {
      const todayStr = getTodayString()
      if (value >= todayStr) {
        setErrors((prev) => ({ ...prev, due_date: "" }))
      }
    }
  }

  const extractErrorMessage = (data) => {
    if (!data) return null
    if (typeof data.error === 'string') return data.error
    if (typeof data.detail === 'string') return data.detail
    if (typeof data.message === 'string') return data.message
    if (data.errors) {
      if (typeof data.errors === 'string') return data.errors
      if (typeof data.errors === 'object') {
        const values = Object.values(data.errors).flat()
        if (values.length > 0 && typeof values[0] === 'string') {
          return values[0]
        }
      }
    }
    return null
  }

  const submitHandler = async () => {
    if (isLoading) return

    setApiError(null)

    const newErrors = {}
    const trimmedAssignment = assignment.trim()

    if (!trimmedAssignment) {
      newErrors.assignment = "Assignment name is required"
    }

    if (!due_date) {
      newErrors.due_date = "Due date is required"
    } else {
      const parts = due_date.split('-').map(Number)
      if (parts.length !== 3 || parts.some(isNaN)) {
        newErrors.due_date = "Please enter a valid date"
      } else {
        const [year, month, day] = parts
        const dateObj = new Date(year, month - 1, day)
        if (
          isNaN(dateObj.getTime()) ||
          dateObj.getFullYear() !== year ||
          dateObj.getMonth() !== month - 1 ||
          dateObj.getDate() !== day
        ) {
          newErrors.due_date = "Please enter a valid date"
        } else {
          const todayStr = getTodayString()
          if (due_date < todayStr) {
            newErrors.due_date = "Due date cannot be before today"
          }
        }
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    setErrors({})
    setDashboardData(null)
    setIsLoading(true)

    try {
      const data = {
        assignment_name: assignment,
        due_date: due_date
      }
      const response = await fetch("http://127.0.0.1:8000/api/assignment-reminder/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })

      if (!response.ok) {
        let backendMessage = null
        try {
          const errorData = await response.json()
          backendMessage = extractErrorMessage(errorData)
        } catch {
          // Response body was not valid JSON
        }
        setApiError(backendMessage || "Something went wrong. Please try again.")
        return
      }

      const result = await response.json()
      console.log(result)
      setDashboardData(result)
      setApiError(null)
    } catch (err) {
      if (
        err instanceof TypeError ||
        (err && typeof err.message === 'string' && (
          err.message.toLowerCase().includes('fetch') ||
          err.message.toLowerCase().includes('network')
        ))
      ) {
        setApiError("Unable to connect to the server. Please try again.")
      } else {
        setApiError("Something went wrong. Please try again.")
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="assignment-container">
      <header className="assignment-header">
        <h1 className="assignment-title">AI Assignment Reminder</h1>
        <p className="assignment-subtitle">
          Generate and send personalized reminders to students who haven't submitted.
        </p>
      </header>

      <section className="assignment-card" aria-label="Assignment Reminder Form">
        <div className="form-field">
          <label htmlFor="assignment-name" className="field-label">
            Assignment Name
          </label>
          <input
            id="assignment-name"
            type="text"
            className={`form-input ${errors.assignment ? 'has-error' : ''}`}
            placeholder="Enter assignment name"
            value={assignment}
            onChange={handleAssignmentChange}
            disabled={isLoading}
            aria-invalid={!!errors.assignment}
            aria-describedby={errors.assignment ? "assignment-error" : undefined}
          />
          {errors.assignment && (
            <span id="assignment-error" className="field-error" role="alert">
              {errors.assignment}
            </span>
          )}
        </div>

        <div className="form-field">
          <label htmlFor="due-date" className="field-label">
            Due Date
          </label>
          <input
            id="due-date"
            type="date"
            className={`form-input form-input-date ${errors.due_date ? 'has-error' : ''}`}
            value={due_date}
            min={getTodayString()}
            onChange={handleDateChange}
            disabled={isLoading}
            aria-invalid={!!errors.due_date}
            aria-describedby={errors.due_date ? "due-date-error" : undefined}
          />
          {errors.due_date && (
            <span id="due-date-error" className="field-error" role="alert">
              {errors.due_date}
            </span>
          )}
        </div>

        <button
          type="button"
          className="submit-button"
          onClick={submitHandler}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="button-spinner" aria-hidden="true"></span>
              <span>Sending reminders...</span>
            </>
          ) : (
            <span>Send Reminders</span>
          )}
        </button>
      </section>

      {/* Inline API Error Banner */}
      {apiError && !isLoading && (
        <aside className="api-error-banner" role="alert">
          <span className="api-error-icon" aria-hidden="true">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </span>
          <div className="api-error-content">
            <p className="api-error-message">{apiError}</p>
          </div>
        </aside>
      )}

      {/* Skeleton Dashboard displayed below the form while loading */}
      {isLoading && (
        <section
          className="skeleton-dashboard"
          aria-busy="true"
          aria-label="Loading reminder results"
        >
          {/* Heading skeleton */}
          <div className="skeleton-header">
            <div className="skeleton-box skeleton-title"></div>
            <div className="skeleton-box skeleton-subtitle"></div>
          </div>

          {/* 3 small statistic card skeletons */}
          <div className="skeleton-stats-grid">
            <div className="skeleton-stat-card">
              <div className="skeleton-box skeleton-stat-label"></div>
              <div className="skeleton-box skeleton-stat-val"></div>
            </div>
            <div className="skeleton-stat-card">
              <div className="skeleton-box skeleton-stat-label"></div>
              <div className="skeleton-box skeleton-stat-val"></div>
            </div>
            <div className="skeleton-stat-card">
              <div className="skeleton-box skeleton-stat-label"></div>
              <div className="skeleton-box skeleton-stat-val"></div>
            </div>
          </div>

          {/* 3 student result row skeletons */}
          <div className="skeleton-list">
            <div className="skeleton-row">
              <div className="skeleton-box skeleton-avatar"></div>
              <div className="skeleton-row-content">
                <div className="skeleton-box skeleton-name"></div>
                <div className="skeleton-box skeleton-email"></div>
              </div>
              <div className="skeleton-box skeleton-badge"></div>
            </div>
            <div className="skeleton-row">
              <div className="skeleton-box skeleton-avatar"></div>
              <div className="skeleton-row-content">
                <div className="skeleton-box skeleton-name"></div>
                <div className="skeleton-box skeleton-email"></div>
              </div>
              <div className="skeleton-box skeleton-badge"></div>
            </div>
            <div className="skeleton-row">
              <div className="skeleton-box skeleton-avatar"></div>
              <div className="skeleton-row-content">
                <div className="skeleton-box skeleton-name"></div>
                <div className="skeleton-box skeleton-email"></div>
              </div>
              <div className="skeleton-box skeleton-badge"></div>
            </div>
          </div>
        </section>
      )}

      {/* Results Dashboard displayed after successful API response */}
      {dashboardData && !isLoading && (
        <section className="results-dashboard" aria-label="Reminder Results Dashboard">
          <header className="results-header">
            <span className="results-badge">Execution Summary</span>
            <h2 className="results-title">{dashboardData.assignment_name}</h2>
            <p className="results-due-date">
              Due Date: <span>{dashboardData.due_date}</span>
            </p>
          </header>

          {/* 3 Statistics Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Students</span>
              <span className="stat-value">{dashboardData.results?.total_students ?? 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Sent</span>
              <span className="stat-value stat-value-sent">{dashboardData.results?.sent ?? 0}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Failed</span>
              <span className="stat-value stat-value-failed">{dashboardData.results?.failed ?? 0}</span>
            </div>
          </div>

          {/* Student Results or Empty State */}
          {dashboardData.results?.total_students === 0 ? (
            <div className="empty-results">
              <span className="empty-icon" aria-hidden="true">
                <svg
                  width="22"
                  height="22"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
              </span>
              <h3 className="empty-title">No pending students</h3>
              <p className="empty-desc">Everyone has already submitted this assignment.</p>
            </div>
          ) : (
            <div className="students-section">
              <h3 className="students-section-title">Student Details</h3>
              <div className="student-cards">
                {dashboardData.results?.results?.map((item, index) => {
                  const isSent = item.status === 'sent'
                  return (
                    <div
                      key={item.message_id || `${item.student}-${index}`}
                      className="student-row"
                    >
                      <div className="student-main">
                        <span className="student-name">{item.student}</span>
                        <span
                          className={`status-badge ${
                            isSent ? 'status-sent' : 'status-failed'
                          }`}
                        >
                          <span className="status-dot"></span>
                          {isSent ? 'Sent' : 'Failed'}
                        </span>
                      </div>
                      <div className="student-meta">
                        <span className="student-attempts">
                          {item.attempts === 1 ? '1 attempt' : `${item.attempts ?? 1} attempts`}
                        </span>
                        {isSent && item.message_id && (
                          <span
                            className="student-msg-id"
                            title={`Message ID: ${item.message_id}`}
                          >
                            ID: {item.message_id.length > 20 ? `${item.message_id.slice(0, 18)}...` : item.message_id}
                          </span>
                        )}
                      </div>
                      {!isSent && item.error && (
                        <div className="student-error-note">
                          Error: {item.error}
                        </div>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </section>
      )}
    </main>
  )
}

export default App
