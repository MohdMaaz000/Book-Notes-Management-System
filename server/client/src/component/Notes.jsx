import NoteItem from "./NoteItem"
import { useEffect, useRef, useState } from "react"
import axios from "axios"

import { IoCreateOutline } from "react-icons/io5"
import { useNavigate } from "react-router-dom"

const BACKEND_URL = import.meta.env.VITE_API_URL

function Notes({ bookId }) {
  const navigate = useNavigate()
  const bookNameRef = useRef()
  const warningRef = useRef()
  let [noteList, setNoteList] = useState([])

  const getAllNotes = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/v1/books/${bookId}/notes`, {
        withCredentials: true,
      })
      const totalNote = response.data
      const newNoteList = totalNote.map((item) => ({
        noteId: item._id,
        noteTitle: item.title,
      }))
      setNoteList(newNoteList)
    } catch (error) {
      if (error.response.status === 401) {
        navigate("/login")
      } else if (error.response.status === 404) {
        navigate("/not-found")
      } else {
        // bad-request
        navigate("/")
      }
    }
  }

  useEffect(() => {
    getAllNotes()
  }, [])

  const deleteNote = async (event, noteId) => {
    event.preventDefault()
    try {
      await axios.delete(`${BACKEND_URL}/api/v1/books/${bookId}/notes/${noteId}`, {
        withCredentials: true,
      })
      getAllNotes()
    } catch (error) {
      if (error.response.status === 401) {
        navigate("/login")
      } else if (error.response.status === 404) {
        navigate("/not-found")
      } else {
        navigate("/")
      }
    }
  }

  const createNote = async (event) => {
    event.preventDefault()
    try {
      const title = bookNameRef.current.value
      const response = await axios.post(
        `${BACKEND_URL}/api/v1/books/${bookId}/notes`,
        {
          title: title,
          content: JSON.stringify(""),
        },
        {
          withCredentials: true,
        }
      )

      bookNameRef.current.value = ""

      const noteId = response.data._id

      navigate(`/books/${bookId}/notes/${noteId}`)
    } catch (error) {
      if (error.response.status === 401) {
        navigate("/login")
      } else if (error.response.status === 404) {
        navigate("/not-found")
      } else if (error.response.status === 400) {
        warningRef.current.innerText = "Please provide the note name"
        setTimeout(() => {
          warningRef.current.innerText = ""
        }, 3000)
      }
    }
  }

  return (
    <>
      <center>
        <div ref={warningRef} className="warning-message"></div>
        <div className="container note-input-container">
          <input ref={bookNameRef} type="text"></input>
          <button onClick={createNote} className="btn btn-outline-success">
            <IoCreateOutline /> Add New Note
          </button>
        </div>
        {/* <div className="note-container"> */}
        {noteList.map((item) => (
          <NoteItem
            handleDeleteButton={deleteNote}
            key={item.noteId}
            noteId={item.noteId}
            noteTitle={item.noteTitle}
            bookId={bookId}
          ></NoteItem>
        ))}
        {/* </div> */}
      </center>
    </>
  )
}

export default Notes
