const express = require("express")
const router = express.Router()
const validateBook = require("../middleware/validate-book.js")

const {
  getAllNotes,
  createNote,
  deleteNote,
  getNote,
  updateNote,
} = require("../controller/note")

router
  .route("/:bookId/notes")
  .get(validateBook, getAllNotes)
  .post(validateBook, createNote)
router
  .route("/:bookId/notes/:noteId")
  .get(validateBook, getNote)
  .delete(validateBook, deleteNote)
  .patch(validateBook, updateNote)

module.exports = router
