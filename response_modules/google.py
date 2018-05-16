from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw

stopwords =['define', 'definicion', 'que','quién','quien', 'es', 'explica',
                 'detalla', 'Aclara', 'dime', '']

def get_response(message):
    """
    This function returns a definition based on a query, in this case the function
    will return a definition as an answer
    :return: String with the answer
    """

    token_list = word_tokenize(str(message), "spanish")
    clean_tokens = []

    for token in token_list:
        token = token.lower()

        if token in stopwords or token in set(sw.words("spanish")):
            continue

        clean_tokens.append(token)

    message = " ".join(clean_tokens)

    return "Buscando: " + message


