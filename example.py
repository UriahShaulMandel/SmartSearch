from word_matcher import WordMatcher
import pandas as pd
import sys

args = sys.argv[1:]

words_df = pd.read_excel(
    input("Please enter the complete file path of the excel file:")
    if not args
    else args[0]
)

word_matcher = WordMatcher(words_df)
print(
    "Note - the pressing enter is only for this example, in the website it will be searched automatically after every key press")

while True:
    search_key = input("Please write text and press enter:\n")
    print([*word_matcher.get_possibilities(search_key)[:5]])
