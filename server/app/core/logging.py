import logging


logger = logging.getLogger("book_notes_management_system")


def configure_logging() -> None:
    if logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
