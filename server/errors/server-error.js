const CustomAPIError = require("./custom-api")

class ServerError extends CustomAPIError {
  constructor(message) {
    super(message)
    this.statusCode = 500
  }
}

module.exports = ServerError
