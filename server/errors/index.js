const CustomAPIError = require("./custom-api")
const UnauthenticatedError = require("./unauthenticated")
const NotFoundError = require("./not-found")
const BadRequestError = require("./bad-request")
const ServerError = require("./server-error")

module.exports = {
  CustomAPIError,
  UnauthenticatedError,
  NotFoundError,
  BadRequestError,
  ServerError,
}
