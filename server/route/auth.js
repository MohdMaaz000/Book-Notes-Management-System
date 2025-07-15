const express = require("express")
const router = express.Router()

const { register, login, logout, profile } = require("../controller/auth")

router.post("/register", register)
router.post("/login", login)
router.get("/logout", logout)
router.get("/", profile)

module.exports = router
