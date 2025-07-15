const { NotFoundError, UnauthenticatedError } = require("../errors")
const asyncWrapper = require("../middleware/async")
const User = require("../model/User")

const setCookie = (res, token) => {
  const expires = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
  res.cookie("token", token, {
    expires: expires,
    httpOnly: true,
    secure: true,
    sameSite: "Strict",
  })
}

const register = asyncWrapper(async (req, res) => {
  const user = await User.create({ ...req.body })

  const token = user.createJWT()
  setCookie(res, token)
  res.status(201).json({ user: { name: user.name }, token })
})

const login = asyncWrapper(async (req, res) => {
  const { email, password } = req.body

  const user = await User.findOne({ email })
  if (!user) {
    throw new NotFoundError(`No user with email ${email}`)
  }

  const isPasswordCorrect = await user.comparePassword(password)
  if (!isPasswordCorrect) {
    throw new UnauthenticatedError("Password does not match")
  }

  const token = user.createJWT()
  setCookie(res, token)
  res.status(200).json({ user: { name: user.name }, token })
})

const logout = (req, res) => {
  res.clearCookie("token")
  res.json({ message: "Logged out successfully" })
}

const profile = (req, res) => {
  res.status(200).json({ username: req.user.name })
}

module.exports = {
  register,
  login,
  logout,
  profile,
}
