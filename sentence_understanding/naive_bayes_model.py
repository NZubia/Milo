#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics

from text_preprocessing.text_preprocessor import TextPreprocessor

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TIMEDIFF = 0  # max time in seconds for verification of last training
WEEKDAY = 6  # day of week allow to auto training    5: saturday 6: sunday
MINPROB = 0.001  # min of probability for include a class i n options


def train_model():
    """
    This function train a naive bayes model
    :return: trained model
    """

    # load training data
    training_data, training_targets, testing_data, test_targets = load_training_data()

    # Define Bag of Words
    count_vectorizer = CountVectorizer(max_features=5000, strip_accents='ascii', lowercase=True)
    count_vectorizer.fit(training_data)

    training_feature_vector = count_vectorizer.transform(training_data)
    test_feature_vector = count_vectorizer.transform(testing_data)

    # model declaration and training
    naive_bayes_model = GaussianNB()
    naive_bayes_model.fit(training_feature_vector.toarray(), training_targets)

    # model measure
    test_data_predicted = naive_bayes_model.predict(test_feature_vector.toarray())

    cm = metrics.confusion_matrix(test_targets, test_data_predicted)
    score = metrics.accuracy_score(test_targets, test_data_predicted)

    logger.debug("TRAIN SCORE: %s", score)

    # TODO: save model

    return naive_bayes_model, count_vectorizer


def predict_label(message):
    """
    This function load the model saved and return the predicted label.
    If model exists the function will load the model, else the model is trained
    :param message: message to predict label
    :return: String with predicted label
    """

    # load model
    model, count_vectorizer = load_model()

    # BOW transformation
    sentence_feature_vector = count_vectorizer.transform([message])

    if sentence_feature_vector.nnz != 0:
        classes = model.classes_
        classif = []

        # predict label and its score
        model_proba = model.predict_proba(sentence_feature_vector.toarray())

        for i, item in enumerate(model_proba[0]):
            if item > MINPROB:
                classif.append([item, classes[i]])

        classif = sorted(classif, key=lambda x: x[0])
        classif.reverse()

        # Get best class and best score
        best_prob_score = classif[0][0]
        best_class = classif[0][1]

        return best_class, best_prob_score
    else:
        return 'unknown', 0.0


def load_model():
    """
    This function load the machine learning model
    :return: trained naive bayes model
    """

    # TODO: Save and get trained model
    trained_model = False

    if not trained_model:
        model, count_vectorizer = train_model()

    return [model, count_vectorizer]


def load_training_data():
    """
    This function loads the data belonging to milo skills
    """
    training_data = {
        'saludos':{
            'intents':['Hola', 'Ola', 'Saludos', 'Buen día', 'Buenos días', 'Buenas tardes',
                     'Buenas noches', 'Hi', 'Hey', 'Abby', 'Hola, ¿cómo estás?', 'Hola, ¿cómo te va?',
                     '¿Cómo estás?', '¿Cómo te va?', '¿Cuál es tu nombre?'],
            'examples':['Hola', 'Ola', 'Saludos', 'Buen día', 'Buenos días', 'Buenas tardes',
                      'Buenas noches', 'Hi', 'Hey', 'Abby', 'Hola, ¿cómo estás?', 'Hola, ¿cómo te va?',
                      '¿Cómo estás?', '¿Cómo te va?', '¿Cuál es tu nombre?']
        },
        'despedidas':{
            'intents':['Adios', 'Bye', 'Nos vemos', 'Hasta pronto', 'Hasta luego'],
            'examples':['Adios', 'Bye', 'Nos vemos', 'Hasta pronto', 'Hasta luego']
        },
        'google':{
            'intents': ['Define que es',"", 'Definicion de', 'Que es','Quién es','Quien es', 'A que se refiere con', 'Explica que es',
                 'Detalla que es', 'Aclara que es', 'Tengo duda con', 'Termino', 'Dime que es'],
            'examples': ['Define que es cheque','cheque', 'Definicion de cheque', 'Que es cheque','Quién es cheque','Quien es cheque', 'A que se refiere con cheque',
                    'Explica que es cheque', 'Detalla que es cheque', 'Aclara que es cheque', 'Tengo duda con cheque',
                    'Termino cheque', 'Dime que es cheque']
        },
        'agradecimientos':{
            'intents':['Gracias', 'Te lo agradezco'],
            'examples': ['Gracias', 'Te lo agradezco']
        }
    }

    # Generating training and testing data
    train_data = []
    train_target_data = []

    test_data = []
    test_target_data = []

    text_clening_model = TextPreprocessor()

    # TODO Improve performance
    # Create array with data and targets
    for skill in training_data:

        skill_dict = training_data.get(skill)

        for intent in skill_dict.get('intents'):
            # intent=text_clening_model.get_preprocessing_message(intent)
            for i in range(5):
                train_data.append(intent)
                train_target_data.append(skill)
        for example in skill_dict.get('examples'):
            # example=text_clening_model.get_preprocessing_message(example)
            for i in range(2):
                test_data.append(example)
                test_target_data.append(skill)

    return train_data, train_target_data, test_data, test_target_data
