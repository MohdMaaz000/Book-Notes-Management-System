const mongoose = require("mongoose")

const BookSchema = new mongoose.Schema({
  subject: {
    type: String,
    trim: true,
    required: [true, "Please provide subject name"],
    minlength: 3,
    maxlength: 50,
  },
  createdBy: {
    type: mongoose.Types.ObjectId,
    ref: "User",
    required: [true, "Please provide user"],
  },
})

module.exports = mongoose.model("Book", BookSchema)
