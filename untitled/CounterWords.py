import re
import io


class CounterWords:

    def __init__(self, path):
        self.word_dict = dict()

        with io.open(path, encoding="utf-8") as f:
            data = f.read()
            words = [single.lower() for single in re.findall("\w+", data)]
            for word in words:
                self.word_dict[word] = self.word_dict.get(word, 0) + 1

    def word_frequency(self, n):
        assert n > 0, "n should be large than 0"
        word_sort = sorted(self.word_dict.items(), key=lambda item:item[1], reverse=True)
        return word_sort[:n]





def run():
    print("333")
    top_common_word = CounterWords("CounterWords.py").word_frequency(4)
    print("The top used words:")
    for word in top_common_word:
        print(word)


if __name__ == "__main__":
    run()