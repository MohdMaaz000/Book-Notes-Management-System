const errorHandlerMiddleware = (err, req, res, next) => {
  // don't know the kind of error then sending the message with status: internal server error
  const customError = {
    msg: err.message || "Something went wrong try again later",
    statusCode: err.statusCode || 500,
  }

  // note title is compulsory to provide if not provide handling the error
  // sending: bad error response
  if (err.name === "ValidationError") {
    customError.msg = Object.values(err.errors)
      .map((item) => item.message)
      .join(", ")

    customError.statusCode = 400
  }

  // handling the error of types when one user trying to register with the email which already exists in the databasae
  // sending: bad error response
  if (err.code && err.code === 11000) {
    customError.msg = `Duplicate value entered for the ${Object.keys(
      err.keyValue
    )}, please provide another value`
    customError.statusCode = 400
  }

  // When the user messed up with the boookId / or the noteId format of mongodb
  // sending: not found response
  if (err.name == "CastError") {
    customError.msg = `No item found with value ${err.value}`
    customError.statusCode = 404
  }

  // return res.status(500).json({ err })
  return res.status(customError.statusCode).json({ msg: customError.msg })
}

module.exports = errorHandlerMiddleware
