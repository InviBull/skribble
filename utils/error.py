import logging

def NotebookNotFoundError(error):
    logging.error(error)

def IntegrityError(error):
    logging.error(error)

def ConnectError(error):
    logging.error(error)
