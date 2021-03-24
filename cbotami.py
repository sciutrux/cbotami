from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance, JaccardSimilarity, SpacySimilarity
from chatterbot.response_selection import get_first_response, get_most_frequent_response, get_random_response
from chatterbot.filters import get_recent_repeated_responses
from chatterbot.conversation import Statement

# from comparisons import CustomLevenshteinDistance

# override Chatterbot PosLemmaTagger
from tagging import CustomPosLemmaTagger

# add "JustMyCode": false into launch.json to debug Chatterbot code
# under \Lib\site-packages\chatterbot

class CBotAmI():
    """
    Conversational dialog chat bot.
    """

    def __init__(self, config_data):

        # TODO - in specific_response.py can_process() expects to compare to a statement,
        # not text str?
        # does not work with Statement either - bug?
        input_text_statement = Statement(text=config_data.specificResponseAdapter.input_text)

        read_only = False
        if config_data.read_only: 
            read_only = True

        self.bot = ChatBot(
            config_data.bot_name,
            storage_adapter = 'chatterbot.storage.' + config_data.storage_adapter,
            database_uri = config_data.database_uri,
            preprocessors = [
                'chatterbot.preprocessors.clean_whitespace'
            ],
            logic_adapters = [
                'chatterbot.logic.MathematicalEvaluation',
                # UnitConversion needs pint installed
                # 'chatterbot.logic.UnitConversion',
                # TimeLogic needs nltk installed
                # 'chatterbot.logic.TimeLogicAdapter',
                # 'chatterbot.logic.BestMatch',
                {
                    'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                    'input_text': input_text_statement,
                    'output_text': config_data.specificResponseAdapter.output_text
                },
                # {
                #     'import_path': 'chatterbot.logic.BestMatch',
                #     'default_response': config_data.bestMatch.default_response,
                #     'maximum_similarity_threshold': config_data.bestMatch.maximum_similarity_threshold
                # },
                {
                    'import_path': 'best_match.CustomBestMatch',
                    'default_response': config_data.bestMatch.default_response,
                    'maximum_similarity_threshold': config_data.bestMatch.maximum_similarity_threshold
                }
            ],
            filters = [
                get_recent_repeated_responses
            ],
            # options for statement comparison:
            # - LevenshteinDistance
            # - SpacySimilarity
            # - JaccardSimilarity
            statement_comparison_function = SpacySimilarity,
            # options for response selection:
            # - get_first_response
            # - get_most_frequent_response
            # - get_random_response
            response_selection_method = get_most_frequent_response,
            read_only = read_only
        )

        # override Chatterbot PosLemmaTagger get_bigram_pair_string function
        # POS tags were not suitable for how conversations are processed
        custom_tagger = CustomPosLemmaTagger()
        self.bot.storage.tagger.get_bigram_pair_string = custom_tagger.get_bigram_pair_string

    def get_response(self, sentence):
        return self.bot.get_response(sentence)

    def learn_response(self, response, sentence):

        # create statement pair similarly to corpus trainer
        # chatterbot method creates single line with no tagging
        statements_to_create = []
        
        statement_search_text = self.bot.storage.tagger.get_bigram_pair_string(sentence)

        statement = Statement(
            text=sentence,
            search_text=statement_search_text,
            in_response_to=None,
            search_in_response_to='',
            conversation='training'
        )

        # statement.add_tags(*categories)

        # statement = get_preprocessed_statement(statement)

        statements_to_create.append(statement)

        response_search_text = self.bot.storage.tagger.get_bigram_pair_string(response.text)

        response_statement = Statement(
            text=response.text,
            search_text=response_search_text,
            in_response_to=statement.text,
            search_in_response_to=statement_search_text,
            conversation='training'
        )

        # statement.add_tags(*categories)

        # statement = get_preprocessed_statement(statement)

        statements_to_create.append(response_statement)

        self.bot.storage.create_many(statements_to_create)
        # return self.bot.learn_response(response, sentence)