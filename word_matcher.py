import operator
from typing import Dict

import jellyfish


class WordMatcher:
    def __init__(self, options_list):
        self.synonyms_dict = {
            x[1][0].lower(): [y for y in (str(x[1][1]).split(',') if isinstance(x[1][1], str) else [])] for x in
        options_list.iterrows()}

        self.options_list = set(self.synonyms_dict)

    def get_possibilities(self, search_str: str) -> list:
        """
        :param search_str: the string used to search
        :return: list of tuples,
         representing the possibility of each option from the option_list, given in the constructor,
         higher is more possible
        """
        search_str = search_str.lower()
        ret_dict = {option: 0 for option in self.options_list}
        ret_dict = self.scores_pipeline(ret_dict, search_str)
        return sorted(
            ret_dict.items(),
            key=operator.itemgetter(1),
            reverse=True
        )

    def scores_pipeline(self, ret_dict: Dict[str, int], search_str: str) -> Dict[str, int]:
        """

        :param ret_dict: A dictionary with all of the available options, mapped to their default score (0 for now)
        :param search_str: the string used to search
        :return: the dictionary after applying all of the FUNCTIONS
        """
        OPTION_COMPARED_TO_SYNONYMS_CONST = 4

        FUNCTIONS = (
            # The functions of the pipeline, together with their score multiplier. higher means more important
            (WordMatcher.pipeline_equals, 100),
            (WordMatcher.pipeline_starts_with, 70),
            (WordMatcher.pipeline_ends_with, 30),
            (WordMatcher.pipeline_contains, 50),
            (WordMatcher.pipeline_levenshtein, 50),
            (WordMatcher.pipeline_damerau_levenshtein, 50),
        )

        for f in FUNCTIONS:
            ret_dict = {k:
                            v +
                            (f[0](k, search_str) * f[1]) * OPTION_COMPARED_TO_SYNONYMS_CONST +
                            sum([(f[0](kk, search_str) * f[1]) for kk in self.get_synonyms_for_option(k)])

                        for k, v in ret_dict.items()}
        return ret_dict

    def get_synonyms_for_option(self, option: str):
        # option = option.lower()
        # option = ''.join([i for i in option if i.isalpha() or i == " "])
        # options_divided = option.split(" ")
        # options_divided = [option for option in options_divided if option in self.en_words_set]
        # ret = list()
        # for option in options_divided:
        #     synonyms = wordnet.synsets(option)
        #     if len(synonyms) > 0:
        #         syn_iter = synonyms[0].lemma_names()
        #         for synonym in syn_iter:
        #             ret.append(synonym)
        return self.synonyms_dict[option]

    # functions returns 0 - 10
    @staticmethod
    def pipeline_contains(option: str, search_str: str):
        return 10 if search_str in option else 0

    @staticmethod
    def pipeline_equals(option: str, search_str: str):
        return 10 if search_str == option else 0

    @staticmethod
    def pipeline_starts_with(option: str, search_str: str):
        return 10 if option.startswith(search_str) else 0

    @staticmethod
    def pipeline_ends_with(option: str, search_str: str):
        return 10 if option.endswith(search_str) else 0

    @staticmethod
    def pipeline_levenshtein(option: str, search_str: str):
        lv_dist = jellyfish.levenshtein_distance(search_str, option)
        return 0 if lv_dist >= 10 else 10 - lv_dist

    @staticmethod
    def pipeline_damerau_levenshtein(option: str, search_str: str):
        lv_dist = jellyfish.damerau_levenshtein_distance(search_str, option)
        return 0 if lv_dist >= 10 else 10 - lv_dist
