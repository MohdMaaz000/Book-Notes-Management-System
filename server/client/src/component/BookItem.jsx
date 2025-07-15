import { FaRegFolderOpen } from "react-icons/fa"

import { MdOutlineLibraryBooks } from "react-icons/md"
import Notes from "./Notes"
import DeleteButton from "./DeleteButton"

const BookItem = ({ bookId, bookName, handleDeleteButton }) => {
  return (
    <>
      <div className="single-book">
        <div>
          <h4>
            <MdOutlineLibraryBooks /> {bookName}
          </h4>
        </div>

        <div>
          <button
            className="btn btn-outline-dark"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target={`#${bookId}`}
            aria-expanded="false"
            aria-controls={"collapseExample"}
          >
            <FaRegFolderOpen />
          </button>

          <DeleteButton
            handleDeleteButton={handleDeleteButton}
            targetName={bookName}
            targetId={bookId}
          ></DeleteButton>
        </div>
      </div>

      <div className="collapse" id={bookId}>
        <div className="card card-body">
          <Notes bookId={bookId}></Notes>
        </div>
      </div>
    </>
  )
}

export default BookItem
