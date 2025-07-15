import { MdDelete } from "react-icons/md"

function DeleteButton({ handleDeleteButton, targetName, targetId }) {
  return (
    <>
      <button
        type="button"
        className="btn btn-outline-dark"
        data-bs-toggle="modal"
        data-bs-target={`#d${targetId}`}
      >
        <MdDelete />
      </button>

      <div
        className="modal fade"
        id={`d${targetId}`}
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabIndex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h1 className="modal-title fs-5" id="staticBackdropLabel">
                {targetName}
              </h1>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">Are you sure you want to delete.</div>
            <div className="modal-footer">
              <button
                onClick={(event) => handleDeleteButton(event, targetId)}
                type="button"
                className="btn btn-primary"
                data-bs-dismiss="modal"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default DeleteButton
