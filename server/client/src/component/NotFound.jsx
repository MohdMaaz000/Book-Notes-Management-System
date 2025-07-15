import { Link } from "react-router-dom"

function NotFound() {
  return (
    <center>
      <h1>
        404 <br />
        This is not the web page <br /> you are looking for.
      </h1>
      <Link className="btn btn-primary" to="/">
        Go to home
      </Link>
    </center>
  )
}

export default NotFound
