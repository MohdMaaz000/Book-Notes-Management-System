import { Link, useNavigate } from "react-router-dom"
import groupImage from "../assets/books.png"

function Home() {
  const navigate = useNavigate()

  const handleSignUpClick = (event) => {
    event.preventDefault()
    navigate("/login")
  }

  return (
    <div className="container big-container">
      <div className="info-container">
        <h2>
          Welcome to <span className="home-textmate">Textmate</span>
          <br />
          <span className="home-textmate-bottom">
            Your Ultimate Note-Taking Companion
          </span>
        </h2>
        <p className="display-6">
          Transforming the Way You Learn and Organize Information
        </p>
        <p>
          Get Started Today Ready to revolutionize your note-taking experience?
          Sign up now and discover how Textmate can make your learning and
          organization more efficient and enjoyable.
        </p>
        <div className="home-btn-container">
          <Link to="/register" className="btn btn-primary">
            Sign Up
          </Link>
          <Link to="/books" className="btn btn-outline-primary">
            Go To Book
          </Link>
        </div>
      </div>
      <div className="home-img-container">
        <img className="home-img" src={groupImage} alt="" />
      </div>
    </div>
  )
}

export default Home
