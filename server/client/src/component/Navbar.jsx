import axios from "axios"
import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"

const BACKEND_URL = import.meta.env.VITE_API_URL

function Navbar() {
  const navigate = useNavigate()
  const [username, setUsername] = useState()

  useEffect(() => {
    const getProfile = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/api/v1/profile`, {
          withCredentials: true,
        })
        setUsername(response.data.username)
      } catch (error) {
        if (error.response) {
          if (error.response.status === 401) {
            navigate("/login")
          } else {
            navigate("/")
          }
        }
      }
    }

    getProfile()
  }, [])

  const handleLogout = async (event) => {
    event.preventDefault()

    try {
      const response = await axios.get(`${BACKEND_URL}/api/v1/auth/logout`, {
        withCredentials: true,
      })
      // console.log(response)
      navigate("/")
    } catch (error) {
      // console.log(error)
      navigate("/")
    }
  }

  return (
    <nav className="navbar fixed-top navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <span className="navbar-brand">{username}</span>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <Link
                to="/books"
                className="nav-link active go-to-book-btn"
                aria-current="page"
              >
                Books
              </Link>
            </li>
          </ul>
          <form className="d-flex">
            <button
              onClick={handleLogout}
              className="btn btn-primary"
              type="button"
            >
              Logout
            </button>
          </form>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
