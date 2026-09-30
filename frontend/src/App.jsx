import { useState,useEffect } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'

function App() {
  const [assignment,setAssignment] = useState("")
  const [due_date,setDate] = useState("")
  const submitHandler = async()=>{
    const data = {
      assignment_name:assignment,
      due_date:due_date
    }
        const response = await fetch("http://127.0.0.1:8000/api/assignment-reminder/",{
          method:"POST",
          headers:{
            "Content-Type": "application/json"
          },
          body:JSON.stringify(data)
        })

        const result = await response.json()
        console.log(result)
  }
  return (
    <>
    <div>
      <input type='text' placeholder='assignment name' value={assignment} onChange={(e)=>setAssignment(e.target.value)}/>
      <input type="date" placeholder='due date' value={due_date} onChange={(e)=>setDate(e.target.value)}/>
      <button onClick={submitHandler}>send reminder</button>

    </div>
    </>
  )
}

export default App
