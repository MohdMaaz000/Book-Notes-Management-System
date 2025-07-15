const Book = require("../model/Book")
const { NotFoundError } = require("../errors")

// validating the key pair <userId, bookId> so that no other user has acess to other users books
const validateBook = async (req, res, next) => {
  const { bookId } = req.params
  const { userId } = req.user
  const book = await Book.find({ _id: bookId, createdBy: userId })
  if (book.length < 1) {
    throw new NotFoundError(`${req.user.name} has no book with book-id: ${bookId}`)
  }

  next()
}

module.exports = validateBook
