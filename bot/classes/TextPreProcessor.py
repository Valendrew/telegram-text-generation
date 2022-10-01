from collections.abc import Iterator
from bot.regexes import EXPRESSIONS
import re


class TextPreProcessor:
    def __init__(self, **kwargs) -> None:
        self.regexes = {k.lower(): re.compile(v) for k, v in EXPRESSIONS.items()}

    def pre_process_doc(self, original_data: str) -> list[str]:
        # lowercase
        data = original_data.lower()

        # spaces
        data = self.regexes["spaces"].sub(" ", data)

        # punctuations to tokenize
        data = self.regexes["add_symbols"].sub(r" \1 ", data)

        # punctuations to remove
        data = self.regexes["remove_symbols"].sub(r" ", data)

        # elongated
        data = self.regexes["elongated"].sub(r"\1", data)

        # emojis
        # data = self.regexes["emojis"].sub(" ", data)

        data = self.regexes["spaces"].sub(" ", data)

        return data.strip().split(" ")

    def pre_process_docs(self, raw_data: list[str]) -> Iterator[list[str]]:
        from tqdm import tqdm

        for d in tqdm(raw_data, desc="Pre-processing messages"):
            yield self.pre_process_doc(d)
