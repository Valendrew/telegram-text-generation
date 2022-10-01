import random

class NGramModel(object):
    def __init__(self, n):
        self.n = n

        # dictionary that keeps list of candidate words given context
        self.context = {}

        # keeps track of how many times ngram has appeared in the text before
        self.ngram_counter = {}

    def get_ngrams(self, tokens: list[str]) -> list:
        """
        :param n: n-gram size
        :param tokens: tokenized sentence
        :return: list of ngrams

        ngrams of tuple form: ((previous wordS!), target word)
        """

        tokens.append('<END>')
        tokens = (self.n - 1) * ["<START>"] + tokens
        l = [
            (tuple([tokens[i - p - 1] for p in reversed(range(self.n  - 1))]), tokens[i])
            for i in range(self.n  - 1, len(tokens))
        ]
        return l

    def update(self, sentence: list[str]) -> None:
        """
        Updates Language Model
        :param sentence: input text
        """
        ngrams = self.get_ngrams(sentence)
        for ngram in ngrams:
            if ngram in self.ngram_counter:
                self.ngram_counter[ngram] += 1.0
            else:
                self.ngram_counter[ngram] = 1.0

            prev_words, target_word = ngram
            if prev_words in self.context:
                self.context[prev_words].append(target_word)
            else:
                self.context[prev_words] = [target_word]

    def prob(self, context, token):
        """
        Calculates probability of a candidate token to be generated given a context
        :return: conditional probability
        """
        try:
            count_of_token = self.ngram_counter[(context, token)]
            count_of_context = float(len(self.context[context]))
            result = count_of_token / count_of_context

        except KeyError:
            result = 0.0
        return result

    def random_token(self, context):
        """
        Given a context we "semi-randomly" select the next word to append in a sequence
        :param context:
        :return:
        """
        r = random.random()
        map_to_probs = {}
        token_of_interest = self.context[context]
        for token in token_of_interest:
            map_to_probs[token] = self.prob(context, token)

        summ = 0
        for token in sorted(map_to_probs):
            summ += map_to_probs[token]
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
            obj = self.random_token(tuple(context_queue))
            if obj == "<END>":
                print("Found END")
                break

            result.append(obj)
            if n > 1:
                context_queue.pop(0)
                if obj == ".":
                    context_queue = (n - 1) * ["<START>"]
                else:
                    context_queue.append(obj)
        return " ".join(result)
