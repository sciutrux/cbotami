# custom LogigAdapter based on Chatterbot BestMatch()
# using custom search algorithm

from chatterbot.logic import LogicAdapter
from chatterbot import filters

from search import CustomIndexedTextSearch

# limit initial search results
MAX_RESULTS = 10

class CustomBestMatch(LogicAdapter):
    """
    A logic adapter that returns a response based on known responses to
    the closest matches to the input statement.

    :param excluded_words:
        The excluded_words parameter allows a list of words to be set that will
        prevent the logic adapter from returning statements that have text
        containing any of those words. This can be useful for preventing your
        chat bot from saying swears when it is being demonstrated in front of
        an audience.
        Defaults to None
    :type excluded_words: list
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.excluded_words = kwargs.get('excluded_words')

        # set up custom search algorithm
        custom_search_algorithm = CustomIndexedTextSearch(chatbot, **kwargs)

        self.chatbot.search_algorithms[custom_search_algorithm.name] = custom_search_algorithm

        self.chatbot.search_algorithm_name = CustomIndexedTextSearch.name

        self.chatbot.search_algorithm = self.chatbot.search_algorithms[
            self.chatbot.search_algorithm_name
        ]

    def process(self, input_statement, additional_response_selection_parameters=None):

        no_responses_found = True

        search_results = self.search_algorithm.search(input_statement)

        results_by_confidence = []

        # input_statement is used as a last resort
        results_by_confidence.append(input_statement)

        nbr_of_results = 0

        # get search results and sort by confidence
        for result in search_results:

            # add result to list, keep list sorted by confidence descending
            for i in range(len(results_by_confidence)):
                if result.confidence > results_by_confidence[i].confidence:
                    results_by_confidence.insert(i, result)
                    break

            nbr_of_results = nbr_of_results + 1
            if nbr_of_results >= MAX_RESULTS:
                break

        recent_repeated_responses = filters.get_recent_repeated_responses(
            self.chatbot,
            input_statement.conversation
        )

        for index, recent_repeated_response in enumerate(recent_repeated_responses):
            self.chatbot.logger.info('{}. Excluding recent repeated response of "{}"'.format(
                index, recent_repeated_response
            ))

        # search for a response for results sorted by descending confidence
        # not all results have a response
        for closest_match in results_by_confidence:

            self.chatbot.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
                closest_match.text, input_statement.text, closest_match.confidence
            ))

            response_selection_parameters = {
                'search_in_response_to': closest_match.search_text,
                'exclude_text': recent_repeated_responses,
                'exclude_text_words': self.excluded_words
            }

            if additional_response_selection_parameters:
                response_selection_parameters.update(additional_response_selection_parameters)

            # get all statements that are in response to the closest match
            response_list = list(self.chatbot.storage.filter(**response_selection_parameters))

            if not response_list:
                self.chatbot.logger.info('No responses found, continuing.')
                continue

            if response_list:
                self.chatbot.logger.info(
                    'Selecting response from {} optimal responses.'.format(
                        len(response_list)
                    )
                )

                response = self.select_response(
                    input_statement,
                    response_list,
                    self.chatbot.storage
                )

                response.confidence = closest_match.confidence
                self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))
                no_responses_found = False
                break 
        
        # no responses found, try generating alternate response
        if no_responses_found:

            self.chatbot.logger.info('No responses found. Generating alternate response list.')

            alternate_response_list = []

            alternate_response_selection_parameters = {
                'search_in_response_to': self.chatbot.storage.tagger.get_bigram_pair_string(
                    input_statement.text
                ),
                'exclude_text': recent_repeated_responses,
                'exclude_text_words': self.excluded_words
            }

            if additional_response_selection_parameters:
                alternate_response_selection_parameters.update(additional_response_selection_parameters)

            alternate_response_list = list(self.chatbot.storage.filter(**alternate_response_selection_parameters))

            if alternate_response_list:
                self.chatbot.logger.info(
                    'Selecting response from {} optimal alternate responses.'.format(
                        len(alternate_response_list)
                    )
                )
                response = self.select_response(
                    input_statement,
                    alternate_response_list,
                    self.chatbot.storage
                )

                # response.confidence = closest_match.confidence
                self.chatbot.logger.info('Alternate response selected. Using "{}"'.format(response.text))
                no_responses_found = False

        # no responses found, use default response
        if no_responses_found:
            response = self.get_default_response(input_statement)

        return response
