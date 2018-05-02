
def get_response():
    """
    This function returns a greeting based on a query
    :return: String with the answer
    """

    answer = _get_agradecimiento()

    return answer


# TODO unit testing
def _get_agradecimiento():
    """
    Get greeting answer from data base based on context Info
    :return: info object
    """

    answer = "¡Un gusto haberte ayudado! Si necesitas algo mas no dudes en preguntarme."

    return answer
