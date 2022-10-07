from collections.abc import Iterator
import re

from ..regexes import EXPRESSIONS


class TextPreProcessor:
    def __init__(self, **kwargs) -> None:
        self.regexes = {k.lower(): re.compile(v) for k, v in EXPRESSIONS.items()}

    def preprocess(self, original_data: str) -> list[str]:
        # lowercase
        data = original_data.lower()
        data = self.regexes["spaces"].sub(" ", data)
        data = self.regexes["add_symbols"].sub(r" \1 ", data)
        data = self.regexes["remove_symbols"].sub(r" ", data)
        data = self.regexes["elongated"].sub(r"\1", data)
        # data = self.regexes["emojis"].sub(" ", data)
        data = self.regexes["spaces"].sub(" ", data)
        data = data.strip()
        return data.split(" ") if data != "" else list()

    def preprocess_docs(self, raw_data: list[str]) -> Iterator[list[str]]:
        from tqdm import tqdm

        for d in tqdm(raw_data, desc="Pre-processing messages"):
            yield self.preprocess(d)
