from collections import Counter
import random
from abc import ABC, abstractmethod
import sys
from bot.classes import TextPreProcessor
from bot.classes.TokenNode import TokenNode


class NGramModelTrie:
    def __init__(self, n, tokenizer: bool = False):
        if n <= 0:
            raise Exception("N not valid")

        self.n = n

        self.tokenizer = TextPreProcessor() if tokenizer else None

        # dictionary that keeps list of candidate words given context
        self.root = TokenNode("")

    def train(self, sentences: list[str]):
        """Trains the n-gram model.

        Args
            sentences (list[str]): list of sentences
        """
        from tqdm import tqdm

        ngrams = [
            ngram
            for sentence in tqdm(sentences, desc="Pre-processing messages")
            for ngram in self.tokenize_ngram(sentence)
            if len(ngram) > 0
        ]
        counter = Counter(ngrams)
        for gram in tqdm(counter, "Creating the ngram model"):
            count = counter[gram]
            self.add_gram(gram, count)

            if gram[-1] == "<e>":
                for i in range(self.n - 1):
                    sub_gram = gram[i + 1 :]
                    self.add_gram(sub_gram, count)

    def tokenize_ngram(self, sentence: str) -> list[tuple[str]]:
        """Tokenize a sentence and return its ngrams

        Args:
            sentence (str): _description_

        Returns:
            list[tuple[str]]: _description_
        """
        if self.tokenizer is not None:
            tokens = self.tokenizer.pre_process_doc(sentence)
        else:
            tokens = sentence.split()

        if len(tokens) == 0:
            return list()

        if self.n == 1:
            return [(token,) for token in tokens]

        for _ in range(self.n - 1):
            tokens.insert(0, "<START>")
        tokens.append("<END>")
        sequences = [tokens[i:] for i in range(self.n)]

        return [ngram for ngram in zip(*sequences)]

    def add_gram(self, gram, count):
        if not gram:
            return

        node = self.root
        for word in gram:
            node.count += count
            if not node.has_child(word):
                new_node = TokenNode(word)
                node.add_child(new_node)
            node = node.get_child(word)
        node.count += count

    def get_vocab(self):
        """Return the vocabulary."""
        return self.root.children

    def get_vocab_size(self):
        """Return the size of vocabulary."""
        return self.root.num_children()

    def get_count(self, gram):
        """Given a n-gram as list of words, return its absolute count."""
        node = self.root
        for word in gram:
            node = node.get_child(word)
            if node is None:
                return 0
        return node.count

    def get_num_children(self, context):
        """Given a context, returns it N_{+1}(context%)."""
        node = self.root
        for word in context:
            node = node.get_child(word)
            if node is None:
                return 0
        return node.num_children()

    def get_vocab_children(self, context):
        node = self.root
        for word in context:
            node = node.get_child(word)
            if node is None:
                return 0
        return node.children

    def prob(self, token: TokenNode, count_of_context: int):
        """
        Calculates probability of a candidate token to be generated given a context
        :return: conditional probability
        """
        if count_of_context == 0:
            return 0

        result = token.count / float(count_of_context)
        return (token.word, result)

    def random_token(self, context, lambda_coeff: int = 1):
        """
        Given a context we "semi-randomly" select the next word to append in a sequence
        :param context:
        :return:
        """
        r = random.random()
        count_of_context = self.get_count(context)
        if count_of_context == 0:
            raise Exception("Context doesn't exist")

        map_to_probs = dict(
            [
                self.prob(token, count_of_context)
                for token in self.get_vocab_children(context).values()
            ]
        )

        summ = 0
        for token, count in sorted(map_to_probs.items(), key=lambda item: -item[1]):
            summ += count
            if summ > r:
                return token

    def generate_text(self, token_count: int):
        """
        :param token_count: number of words to be produced
        :return: generated text
        """
        n = self.n
        context_queue = (n - 1) * ["<START>"]
        result = []
        for _ in range(token_count):
            token = self.random_token(tuple(context_queue))
            if token == "<END>":
                break

            result.append(token)
            if n > 1:
                context_queue.pop(0)
                if token == ".":
                    context_queue = (n - 1) * ["<START>"]
                else:
                    context_queue.append(token)
        return " ".join(result)
