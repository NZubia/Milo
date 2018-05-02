import string

# Import NLTK tools
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

class TextPreprocessor():
    '''
    Transforms input data by using NLTK tokenization, stemming, and
    other filtering techniques.

    Note: It is possible to create a stopwords corpus and use it.
    Note: words in spanish stopWords corpus =  313
    Note: words in english stopWords corpus =  153
    '''

    def __init__(self, stopwords = None, punct = None, lower = True, strip = True, language ='spanish'):

        self.language = language
        self.lower = lower
        self.strip = strip
        self.stopwords = set(stopwords) if stopwords else set(sw.words(self.language))
        self.punct = set(punct) if punct else set(string.punctuation)

    def sentence_tokenizing(self, sentence):
        '''
        Returns a list of word tokens from a sentence
        e.g I know I need to work in my project, but I have no time. ->
        ['I', 'know', 'I', 'need', 'to', 'work', 'in', 'my',
            'project', ',', 'but', 'I', 'have', 'no', 'time', '.']

        :param sentence: Sentence to tokenize, to prevent errors str()
                            is always used in sentence
        :param language: Language using to tokenize, default is spanish
        '''

        token_list = word_tokenize(str(sentence), self.language)

        return token_list

    def sentence_cleaning(self, tokens):
        '''
        Returns a list of words tokens in lowercase, without punctuation, numbers
        and without stopwords
        e.g ['I', 'know', 'I', 'need', 'to', 'work', 'in', 'my',
            'project', ',', 'but', 'I', 'have', 'no', 'time', '.'] ->

        ['know', 'need', 'work', 'project', have', 'time']


        :param tokens: list of tokens to clean
        '''
        #Apply preprocessing to tokens
        tokens_in_sentence = []

        for token in tokens:

            #Remove punctuation
            if all(char in self.punct for char in token):
                continue

            #Remove numbers
            if token.isdigit():
                continue

            # Transform the token to lowercase and remove spaces
            token = token.lower() if self.lower else token
            token = token.strip() if self.strip else token

            # Remove stopWords
            if token in self.stopwords:
               continue

            tokens_in_sentence.append(token)

        return tokens_in_sentence

    def sentence_stemming(self, tokens):
        '''
        Transform a list of tokens into its original form
        e.g cats - > cat
        e.g cooking -> cook

        :param tokens: tokens list to stemming
        '''
        #Create the stemmer
        stemmer = SnowballStemmer('spanish')

        #stemming tokens
        tokens_in_sentence = []
        for token in tokens:
            tokens_in_sentence.append(stemmer.stem(token))

        return tokens_in_sentence

    def sentence_preprocessing(self, sentence, cleaning = True, stemming = False):
        '''
        Returns a list of tokens from a sentence by applying tokenization.
        After that the list of tokens are cleaning appliying stemming and removing
        stopwords and punctuation, after that a lowercase version ins returned.

        :param sentence: Sentence to tokenize
        :param cleaning: True if you want to clean sentence
        :param stemming: True if you want to stem sentence
        :return: list of clean tokens
        '''

        #Appliying sentence preprocessing
        tokens = self.sentence_tokenizing(sentence)
        tokens = self.sentence_cleaning(tokens) if cleaning is True else tokens
        tokens = self.sentence_stemming(tokens) if stemming is True else tokens

        return tokens

    def get_preprocessing_message(self, sentence, cleaning = True, stemming = False):
        """
        Returns a string with the clean sentence.

        :param sentence: Sentence to tokenize
        :param cleaning: True if you want to clean sentence
        :param stemming: True if you want to stem sentence
        :return: String with clean sentence
        """

        clean_tokens = self.sentence_preprocessing(sentence, cleaning, stemming)

        clean_sentence = ' '.join(clean_tokens)

        return clean_sentence