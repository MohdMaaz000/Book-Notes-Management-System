import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App.jsx"
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import Books from "./component/Books.jsx"
import Layout from "./component/layout/layout.jsx"
import QuillEditor from "./component/QuillEditor.jsx"
import Form from "./component/Form.jsx"
import NotFound from "./component/NotFound.jsx"

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/books",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <Books />,
      },
    ],
  },
  {
    path: "/books/:bookId/notes/:noteId",
    element: <Layout />,
    children: [
      {
        path: "",
        element: <QuillEditor />,
      },
    ],
  },
  {
    path: "/register",
    element: <Form />,
  },
  {
    path: "/login",
    element: <Form />,
  },
  {
    path: "/not-found",
    element: <NotFound />,
  },
])

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)
