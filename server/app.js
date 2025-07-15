const express = require("express")
const app = express()
const connectDB = require("./db/connect.js")
require("express-async-errors")
require("dotenv").config()
const cors = require("cors")
const cookieParser = require("cookie-parser")
const helmet = require("helmet")
const xss = require("xss-clean")

const ServerError = require("./errors/server-error.js")
const errorHandlerMiddleware = require("./middleware/error-handler.js")
const notFoundError = require("./middleware/not-found.js")

const corsOptions = {
  origin: `${process.env.FRONTEND_URL}`, // Frontend's URL
  credentials: true,
}

app.use(cors(corsOptions))
app.use(helmet())
app.use(xss())
app.use(cookieParser())
app.use(express.json())

// routes
const bookRouter = require("./route/book.js")
const noteRouter = require("./route/note.js")
const authRouter = require("./route/auth.js")
const authenticateUser = require("./middleware/authentication.js")


app.use("/api/v1/auth", authRouter)
app.use("/api/v1/profile", authenticateUser, authRouter)
app.use("/api/v1/books", authenticateUser, bookRouter)
app.use("/api/v1/books", authenticateUser, noteRouter)

app.use(notFoundError)
app.use(errorHandlerMiddleware)

const port = process.env.PORT || 3000
const start = async () => {
  try {
    await connectDB(process.env.MONGO_URI)
    app.listen(port, () => {
      console.log(`Server is listening on port ${port}`)
    })
  } catch (error) {
    console.error("Error starting the server:", error.message)
    process.exit(1) // Exit the process if the server fails to start
  }
}


start()
