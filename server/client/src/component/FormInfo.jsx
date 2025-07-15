import { Link, useLocation, useNavigate } from "react-router-dom"
import styles from "./FormInfo.module.css"
import { useRef } from "react"

function Form({ handleFormInfo }) {
  const nameElement = useRef()
  const emailElement = useRef()
  const passwordElement = useRef()

  let isNewUser = window.location.href.includes("register")
  // console.log(isNewUser, window.location.href)
  const handleSubmitButton = (event) => {
    event.preventDefault()
    isNewUser = window.location.href.includes("register")
    if (isNewUser) {
      handleFormInfo(
        nameElement.current.value,
        emailElement.current.value,
        passwordElement.current.value,
        isNewUser
      )
    } else {
      handleFormInfo(
        "",
        emailElement.current.value,
        passwordElement.current.value,
        isNewUser
      )
    }
  }

  return (
    <div className={`container-sm ${styles["form-container"]}`}>
      <form onSubmit={handleSubmitButton}>
        {isNewUser && (
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              className="form-control"
              ref={nameElement}
              id="name"
              label="Name"
              type="text"
              placeholder="Enter name"
            />
          </div>
        )}

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            className="form-control"
            ref={emailElement}
            id="email"
            label="Email address"
            type="email"
            placeholder="Enter email"
          />
          <small id="emailHelp" className="form-text text-muted">
            We'll never share your email with anyone else.
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            className="form-control"
            ref={passwordElement}
            id="password"
            label="Password"
            type="password"
            placeholder="Password"
          />
        </div>

        <button
          className={`${styles["form-btn"]} btn btn-primary`}
          type="submit"
        >
          {isNewUser ? "Register" : "Login"}
        </button>

        <div className="form-group">
          {isNewUser ? (
            <p>
              Already a member?{" "}
              <Link
                to="/login"
                className={`${styles["form-login-register-toggle"]}`}
              >
                Login
              </Link>
            </p>
          ) : (
            <p>
              Not a member yet?{" "}
              <Link
                to="/register"
                className={`${styles["form-login-register-toggle"]}`}
              >
                Register
              </Link>
            </p>
          )}
        </div>
      </form>
    </div>
  )
}

export default Form
