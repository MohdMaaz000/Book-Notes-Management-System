const express = require("express")
const router = express.Router()

const { getAllBooks, createBook, deleteBook } = require("../controller/book")

router.route("/").get(getAllBooks).post(createBook)
router.route("/:bookId").delete(deleteBook)

module.exports = router
