import collections
import logging
import os
import re

from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

from ..regexes import BERT_EXPRESSIONS


class BERTPreProcessor:
    def __init__(self, do_lower_case=True, **kwargs):
        self.do_lower_case = do_lower_case
        self.regexes = {k.lower(): re.compile(v) for k, v in BERT_EXPRESSIONS.items()}

        self.text_processor = TextPreProcessor(
            # terms that will be normalized
            normalize=[
                "url",
                "email",
                "user",
                "percent",
                "money",
                "phone",
                "time",
                "date",
                "number",
            ],
            # terms that will be annotated
            annotate={"hashtag"},
            fix_html=True,  # fix HTML tokens
            unpack_hashtags=True,  # perform word segmentation on hashtags
            # select a tokenizer. You can use SocialTokenizer, or pass your own
            # the tokenizer, should take as input a string and return a list of tokens
            tokenizer=SocialTokenizer(lowercase=True).tokenize,
            dicts=[emoticons],
        )

    def preprocess(self, text: str) -> list[str]:
        if self.do_lower_case:
            text = text.lower()

        text = str(" ".join(self.text_processor.pre_process_doc(text)))
        text = self.regexes["chars"].sub(" ", text)
        text = self.regexes["whitespaces"].sub(" ", text)
        text = self.regexes["words"].sub(r"\1\1", text)
        text = self.regexes["start_wh"].sub("", text)
        text = self.regexes["end_wh"].sub("", text)

        return text.split(" ") if text != "" else list()
