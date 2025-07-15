import { Outlet } from "react-router-dom"
import Navbar from "../Navbar"

const Layout = () => {
  return (
    <>
      <Navbar></Navbar>
      <Outlet></Outlet>
    </>
  )
}

export default Layout
