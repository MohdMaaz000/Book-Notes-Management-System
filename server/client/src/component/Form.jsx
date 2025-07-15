import FormInfo from "./FormInfo"
import axios from "axios"
import { useNavigate } from "react-router-dom"

const BACKEND_URL = import.meta.env.VITE_API_URL

function Form() {
  const navigate = useNavigate()

  const handleFormInfo = async (name, email, password, isNewUser) => {
    const userInfo = {
      email: email,
      password: password,
    }

    if (isNewUser) {
      userInfo.name = name
    }

    // console.log(userInfo)
    // determine the endpoint
    const endpoint = isNewUser ? "register" : "login"
    // console.log(endpoint, userInfo)
    try {
      // POST request to backend API
      const response = await axios.post(
        `${BACKEND_URL}/api/v1/auth/${endpoint}`,
        userInfo,
        { withCredentials: true }
      )
      navigate("/books")
    } catch (error) {
      if (error.response.status === 401) {
        window.alert("Wrong Credntials")
        navigate("/login")
      } else if (error.response.status === 404) {
        navigate("/not-found")
      }
    }
  }

  return <FormInfo handleFormInfo={handleFormInfo} />
}

export default Form
