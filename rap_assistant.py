import random
import urbandictionary
import pronouncing
import pprint
import argparse

class RapAssistant:

    def __init__(self):
        self.rhyme_dict = {}
        self.cached_words = []


    def _parse(self, words):
        """
        Split two-word-phrases.
        """
        
        post_parse = []
        # split 2 word phrases
        for word in words:
            split = word.split(' ')
            if len(split) > 1:
                post_parse.extend(split)
            else:
                post_parse.append(word)

        return post_parse


    def urban_bag(self):
        """
        Returns parsed list of random words from urban dictionary.
        """
        words = self._parse([word.word for word in urbandictionary.random()])

        self.cached_words = words

        return words


    def find_rhymes(self, word_bag=None, num_rhymes=10):
        """
        Accepts list of words or word as parameter, returns dictionary of words and rhymes.
        """
        
        word_bag = self.cached_words if word_bag is None else word_bag

        if isinstance(word_bag, list):
            for word in word_bag:
                rhymes = pronouncing.rhymes(word)
                if len(rhymes) > num_rhymes:
                    self.rhyme_dict[word] = [random.choice(rhymes) for _ in range(num_rhymes)]
                else:
                    self.rhyme_dict[word] = rhymes
        else:
            self.rhyme_dict[word_bag] = pronouncing.rhymes(word_bag)[:num_rhymes]

        return self.rhyme_dict


    def show_pretty_rhyme_dict(self):
        """
        Pretty prints rhyme dictionary.
        """
        if len(self.rhyme_dict) > 0:
            pprint.pprint(self.rhyme_dict)
        else:
            print('Rhyme dictionary contains no words.')
     

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--word', type=str)
    parser.add_argument('-u', '--urban', action='store_true')
    args = vars(parser.parse_args())

    rapper = RapAssistant()

    if args and args['word']:
        rapper.find_rhymes(word_bag=args['word'], num_rhymes=3)
        rapper.show_pretty_rhyme_dict()

    if args and args['urban']:
        words = rapper.urban_bag()
        rapper.find_rhymes(word_bag=words, num_rhymes=3)
        rapper.show_pretty_rhyme_dict()
