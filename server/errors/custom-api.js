class CustomAPIError extends Error {
  constructor(messge) {
    super(messge)
  }
}

module.exports = CustomAPIError
