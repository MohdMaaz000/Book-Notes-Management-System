const Book = require("../model/Book")
const Note = require("../model/Note")
const { NotFoundError } = require("../errors")

// retuning the book that comes under the userId
const getAllBooks = async (req, res) => {
  const { userId } = req.user
  // console.log(userId)

  const books = await Book.find({ createdBy: userId })
  res.status(200).json(books)
}

// creating book under the hood of current active user
const createBook = async (req, res) => {
  const { userId } = req.user
  const { subject } = req.body
  const book = await Book.create({ subject: subject, createdBy: userId })

  res.status(201).json({ book })
}

// deleting book by validating key pair <userId, bookId>
// some user might try to manipulate the data of other user if they know <bookId> of other user
// to avoid that i got to take care that the <bookId> come under the hood of <userId>
const deleteBook = async (req, res) => {
  const { bookId } = req.params
  const { userId } = req.user
  const book = await Book.findOneAndDelete({
    _id: bookId,
    createdBy: userId,
  })

  if (!book) {
    throw new NotFoundError(`No book found with id${userId}`)
  }

  const notes = await Note.deleteMany({ createdUnder: bookId })

  res.status(200).json(book)
}

module.exports = { getAllBooks, createBook, deleteBook }
