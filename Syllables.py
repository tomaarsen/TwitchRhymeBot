
from nltk.corpus import cmudict, stopwords
import string, time, logging, random
logger = logging.getLogger(__name__)

from Database import Database

class Syllables:
    def __init__(self, chan):
        self.dict = cmudict.dict()
        self.stopwords = set(stopwords.words('english'))
        self.db = Database(chan)
        self.syllables = None
        self.level = 3
    
    def attempt_to_rhyme(self, sentence):

        # Remove puncuation, and remove tags
        stripped_sentence = self.__remove_punctuation(self.__remove_tags(sentence))
        split_stripped_sentence = stripped_sentence.split(" ")
        last_word = split_stripped_sentence[-1]

        # Sentences shouldn't be too long
        if len(split_stripped_sentence) > 12:
            #logger.debug(f"Sentence is too long: {len(split_stripped_sentence)} words.")
            return None
        
        # If the last word is not in the cmudict, we can't work with it
        if last_word not in self.dict:
            #logger.debug("Last word isnt in cmudict")
            return None
        
        if len(self.dict[last_word][0]) < 3:
            #logger.debug("Last word has too few sounds")
            return None
        
        # Amount of syllables should not be too high
        #if self.count_syllables(stripped_sentence) > 13:
        #    logger.info(f"Too many syllables: {self.syllables}")
        #    return None

        self.count_syllables(stripped_sentence)

        # Set the level set for the rhyming
        self.get_level(last_word)

        start_t = time.time()
        # Get a list of words that seem to rhyme with the last word
        rhymes = self.get_rhyming_words(last_word)
        # If there are no rhymes found, return None
        if len(rhymes) == 0:
            #logger.debug("No possible rhymes found")
            return None
        #print("Generating rhymes took", time.time() - start_t)

        start_t = time.time()
        out = self.get_sentence(rhymes)
        #print("Generating sentence took", time.time() - start_t)
        return out

        #return (rhymes, self.syllables)
    
    def get_level(self, word):
        # The level is 3, unless the word contains 3 sounds, in which case it is 2.
        # word should never have < 3 sounds. This was ruled out in attempt_to_rhyme()
        self.level = min(3, len(self.dict[word][0]) - 1)

    def get_sentence(self, rhymes):
        # Get the inputs from the rhymes as outputs, and randomly shuffle them
        inputs = self.db.get_inputs(rhymes)
        random.shuffle(inputs)
        
        for tup in inputs:
            items = list(tup)
            result = self.get_previous(items[0], items[1], items, sum([self.__syllable_from_word(word) for word in items]))
            if result is not None:
                return result
        
        return None

    # Recursive Depth-First-Search to get sentence of similar syllable count
    def get_previous(self, input2, output1, total = [], syllable_count = 0):
        # If this path overshot the target, return None
        if syllable_count > self.syllables:
            return None

        # If we have our goal, return with our success
        if syllable_count == self.syllables:
            return " ".join(total)

        # Get new inputs and outputs for recursion
        new_inputs = self.db.get_previous_double(input2, output1)
        new_output1 = input2

        # If no more branches can be found
        if len(new_inputs) == 0:
            return None
        
        for new_input in new_inputs[0]:
            count = self.__syllable_from_word(new_input)
            syllable_count += count
            
            total.insert(0, new_input)
            # Recurse to further branches
            output_from_branch = self.get_previous(new_input, new_output1, total, syllable_count)
            # If the output from these branches are not none (so a successful path was found), return that path
            if output_from_branch is not None:
                return output_from_branch
            # Otherwise wait for the other branches
        
        # If no branches resulted in anything, return False
        return None

    def count_syllables(self, sentence):
        # Get syllable count for entire sentence
        syl_count = 0
        for word in sentence.split(" "):
            temp_count = self.__syllable_from_word(word)
            #print(word, "->", temp_count)
            syl_count += temp_count
        self.syllables = syl_count
        return syl_count
    
    def get_rhyming_words(self, word):
        # Get list of syllables
        syllables = self.dict[word][0]
        relevant_syllables = syllables[-self.level:]
        # Get set of potentially rhyming words
        rhymes = {w for w in self.dict for syl in self.dict[w] if syl[-self.level:] == relevant_syllables and word not in w and w not in word}
        # Return the set of rhymes without any stop words.
        return rhymes - self.stopwords
        
    def __remove_punctuation(self, sentence):
        return sentence.translate(str.maketrans('', '', string.punctuation))

    def __remove_tags(self, sentence):
        # Loop until no more tags can be found
        while sentence.find("@") != -1:
            # Find start of tag
            start = sentence.find("@")
            # Otherwise get the end of the tag (aka the first space after the @ symbol)
            end = sentence.find(" ", start)
            sentence = sentence.replace(sentence[start:end + 1 if end != -1 else end], "")
            print("in while")
        return sentence

    def __syllable_from_word(self, word):
        try:
            # Check NLTK's cmudict for syllable count
            return [len(list(y for y in x if y[-1].isdigit())) for x in self.dict[word.lower()]][0]
        except KeyError:
            # If word is not found in cmudict, use __custom_syllable_from_word
            return self.__custom_syllable_from_word(word)

    def __custom_syllable_from_word(self, word):
        count = 0
        vowels = 'aeiouy'
        word = word.lower()
        if len(word) == 0:
            return count
        # If the word starts with a vowel
        if word[0] in vowels:
            count +=1
        # Loop over rest of word and check for vowels
        for index in range(1,len(word)):
            if word[index] in vowels and word[index-1] not in vowels:
                count +=1
        # One less if it ends with an e
        if word.endswith('e'):
            count -= 1
        # One more if it ends with le
        if word.endswith('le'):
            count+=1
        # If none of the previous were triggered, make it 1
        if count == 0:
            count +=1
        return count
