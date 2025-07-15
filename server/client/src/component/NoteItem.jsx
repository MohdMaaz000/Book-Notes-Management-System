import styles from "./NoteItem.module.css"
import { useNavigate } from "react-router-dom"
import { FaRegNoteSticky } from "react-icons/fa6"
import DeleteButton from "./DeleteButton"

// learning props
const NoteItem = ({ bookId, noteId, noteTitle, handleDeleteButton }) => {
  const navigate = useNavigate()
  const openNote = (event, noteId) => {
    event.preventDefault()
    navigate(`/books/${bookId}/notes/${noteId}`)
  }
  return (
    <div className={`container ${styles["list-item"]}`}>
      <button
        type="button"
        onClick={(event) => openNote(event, noteId)}
        className={`${styles["note-name"]} btn btn-outline-dark`}
      >
        <FaRegNoteSticky /> {noteTitle}
      </button>

      <DeleteButton
        handleDeleteButton={handleDeleteButton}
        targetName={noteTitle}
        targetId={noteId}
      ></DeleteButton>
    </div>
  )
}

export default NoteItem
