const { UnauthenticatedError } = require("../errors")

const jwt = require("jsonwebtoken")

const auth = async (req, res, next) => {
  // console.log(req.signedCookies.token, req.cookies)
  const token = req.cookies?.token

  if (!token) {
    // console.log("No token")
    throw new UnauthenticatedError("Access denied, please login")
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET)
    req.user = { userId: payload.userId, name: payload.name }
    next()
  } catch (error) {
    throw new UnauthenticatedError("Authentication invalid")
  }
}

module.exports = auth
