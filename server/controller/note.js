const Note = require("../model/Note")
const { NotFoundError } = require("../errors")
const Book = require("../model/Book")

// validateBook middleware validated <userId, bookId>
// now i can simply return the notes that come under the <bookId> --- bullshit
// i got to validate the key pair <booId, noteId>
// then it will be fine <userId, bookId> --> <booId, noteId> as they both got the bookId as a common unique key
const getAllNotes = async (req, res) => {
  const { bookId } = req.params
  const notes = await Note.find({ createdUnder: bookId })

  res.status(200).json(notes)
}

// Oh my goodness, this is perfect
const createNote = async (req, res) => {
  const { title, content } = req.body
  const { bookId } = req.params

  const note = await Note.create({ title, content, createdUnder: bookId })
  res.status(200).json(note)
}

// validateBook middleware validating <userId, bookId>
// if validated then key pair <userId, bookId> is valid
// now i need to validate key pair <bookId, noteId> before returninng the note
// i cannot use the only <notId> to validate as it does not gurantees that particular note i.e. <noteId> comes under the <bookId>, it might belongs to some other <bookId>
// The question is that shall i include the <userId> as well in the <NoteSchema> for validation and fileration
// a big no -- why validateBook is already validating the <userId, bookId> i need to validate the <bookId, notedId>
// How come to conclusion : let's see <userId, bookId> --> <bookId, notedId> they got a bookId common, oh my goodness! great!
const getNote = async (req, res) => {
  const { noteId, bookId } = req.params
  const note = await Note.findOne({
    _id: noteId,
    createdUnder: bookId,
  })

  if (!note) {
    throw new NotFoundError(`No note with the id ${noteId}`)
  }

  res.status(200).json(note)
}

// same as the create note
const updateNote = async (req, res) => {
  const { bookId } = req.params
  const { noteId } = req.params
  const { title, content } = req.body

  const note = await Note.findOneAndUpdate(
    { _id: noteId, createdUnder: bookId },
    {
      title: title,
      content: content,
    },
    {
      new: true,
      runValidators: true,
    }

    // why do i need to runValidator? as i make compulsory to provide the title that's why
  )

  if (!note) {
    throw new NotFoundError(`No note with the id ${noteId}`)
  }

  res.status(200).json({ note })
}

// same as createNote
const deleteNote = async (req, res) => {
  const { bookId } = req.params
  const { noteId } = req.params
  const note = await Note.findOneAndDelete({
    _id: noteId,
    createdUnder: bookId,
  })

  if (!note) {
    throw new NotFoundError(`No note with the id ${noteId}`)
  }

  res.status(200).json({ note })
}

module.exports = { getAllNotes, createNote, deleteNote, getNote, updateNote }
