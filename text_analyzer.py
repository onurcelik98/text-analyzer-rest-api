class TextAnalyzer:
    def __init__(self, string, filters):  # Constructor
        self.s = string
        if filters is None:  # No filter specified, response will include all fields.
            self.analytics = {
                "wordCount": self.wordCount(),
                "letters": self.numberOfLetters(),
                "longest": self.longestWord(),
                "avgLength": self.averageWordLength(),
                "duration": self.readingDuration(),
                "medianWordLength": self.medianLength(),
                "medianWord": self.medianWord(),
                "mostCommon": self.top5MostCommon(),
                "language": self.guessLanguage()
            }
        else:  # Filter specified, response will include only the fields specified in filters.
            self.analytics = {}
            if "wordCount" in filters:
                self.analytics["wordCount"] = self.wordCount()
            if "letters" in filters:
                self.analytics["letters"] = self.numberOfLetters()
            if "longest" in filters:
                self.analytics["longest"] = self.longestWord()
            if "avgLength" in filters:
                self.analytics["avgLength"] = self.averageWordLength()
            if "duration" in filters:
                self.analytics["duration"] = self.readingDuration()
            if "medianWordLength" in filters:
                self.analytics["medianWordLength"] = self.medianLength()
            if "medianWord" in filters:
                self.analytics["medianWord"] = self.medianWord()
            if "mostCommon" in filters:
                self.analytics["mostCommon"] = self.top5MostCommon()
            if "language" in filters:
                self.analytics["language"] = self.guessLanguage()

    def wordCount(self):  # Finds number_of_delimiters + 1, where said delimiters are whitespaces, tabs and new lines.
        # Base case
        if len(self.s) < 1:
            return 0
        # Accumulator that counts starting from 1.
        accumulator = 1
        for i in range(0, len(self.s)):
            if self.s[i] in [" ", "\t", "\n"]:
                if i > 0 and not self.s[i-1] in [" ", "\t", "\n"]:
                    accumulator += 1
        return accumulator

    def numberOfLetters(self):  # Assuming that number of letters means number of characters other than new lines
        length = 0              # since it is so in Microsoft Word, Libre Office Writer, and also the provided example.
        for i in range(0, len(self.s)):
            if self.s[i] not in ["\n", "\0"]:
                length += 1
        return length

    def longestWord(self):  # Everytime a non-alphanumeric char is encountered, it applies relaxation on the temporary longest_word.
        # Base case
        if len(self.s) < 1:
            return None
        # Initializations
        max_length = 0
        temp_length = 0
        longest_word = None
        temp_word = ""
        for i in range(0, len(self.s)):
            if self.s[i].isalnum() or self.s[i] in ["'", "-", "_", "/", "’"]:
                temp_length += 1
                temp_word += self.s[i]
                if i == len(self.s) - 1:
                    if temp_length > max_length:
                        max_length = temp_length
                        longest_word = temp_word
                    temp_length = 0
                    temp_word = ""
            else:
                if temp_length > max_length:
                    max_length = temp_length
                    longest_word = temp_word
                temp_length = 0
                temp_word = ""
        return longest_word

    def averageWordLength(self):  # Same strategy with longestWord(), with storing word lengths to later take average of.
        if len(self.s) < 1:
            return 0
        length_array = []
        temp_length = 0
        for i in range(0, len(self.s)):
            if self.s[i].isalnum() or self.s[i] in ["'", "-", "_", "/", "’"]:  # Considering "Alice’s" to be length of 7, not 6.
                temp_length += 1
                if i == len(self.s) - 1:
                    if temp_length > 0:
                        length_array.append(temp_length)
                        temp_length = 0
            else:
                if temp_length > 0:
                    length_array.append(temp_length)
                    temp_length = 0
        return sum(length_array) / len(length_array)

    def readingDuration(self):  # Finds word_count / words_per_second.
        words_per_sec = 200/60  # According to Google, this is the average number of words per minute a person can read.
        return self.wordCount() / words_per_sec

    def medianHelper(self, mode):  # mode == 0: return median length, mode == 1: return median word itself
        # Base case
        if len(self.s) < 1:
            if mode == 0:
                return 0
            else:
                return None
        # Filling the word array
        word_array = []
        temp_word = ""
        for i in range(0, len(self.s)):
            if self.s[i].isalnum() or self.s[i] in ["'", "-", "_", "/", "’"]:
                temp_word += self.s[i]
                if i == len(self.s) - 1:
                    if len(temp_word) > 0:
                        word_array.append(temp_word)
                        temp_word = ""
            else:
                if len(temp_word) > 0:
                    word_array.append(temp_word)
                    temp_word = ""
        # Sorting the word array by ascending length using selection sort
        sorted_word_array = []
        while len(word_array) > 0:
            temp_shortest = word_array[0]
            for e in word_array:
                if len(e) < len(temp_shortest):
                    temp_shortest = e
            sorted_word_array.append(temp_shortest)
            word_array.remove(temp_shortest)
        # Returning the median
        index = (len(sorted_word_array) - 1) // 2
        if mode == 0:
            return len(sorted_word_array[index])
        else:
            return sorted_word_array[index]

    def medianLength(self):
        return self.medianHelper(0)

    def medianWord(self):
        return self.medianHelper(1)

    def top5MostCommon(self):  # Stalemates between words result in favor of the first one to occur in the string.
        # Base case
        if len(self.s) < 1:
            return []
        # Filling the occurrence dictionary
        occurrence_dict = {}
        temp_word = ""
        for i in range(0, len(self.s)):
            if self.s[i].isalnum() or self.s[i] in ["'", "-", "_", "/", "’"]:
                temp_word += self.s[i]
                if i == len(self.s) - 1:
                    if len(temp_word) > 0:
                        if not temp_word.lower() in occurrence_dict:  # converting all to lowercase not to distinguish "apple" from "Apple"
                            occurrence_dict[temp_word.lower()] = 1
                        else:
                            occurrence_dict[temp_word.lower()] += 1
                        temp_word = ""
            else:
                if len(temp_word) > 0:
                    if not temp_word.lower() in occurrence_dict:  # converting all to lowercase not to distinguish "apple" from "Apple"
                        occurrence_dict[temp_word.lower()] = 1
                    else:
                        occurrence_dict[temp_word.lower()] += 1
                    temp_word = ""
        # Retrieving top 5 most common occured words
        top5_array = []
        while len(top5_array) < 5 and len(occurrence_dict) > 0:
            temp_repetition = 0
            temp_word = None
            for key in occurrence_dict:
                if occurrence_dict[key] > temp_repetition:
                    temp_repetition = occurrence_dict[key]
                    temp_word = key
            top5_array.append(temp_word)
            del occurrence_dict[temp_word]
        # Returning the top5_array
        return top5_array

    def anyInString(self, letters):  # Checks whether at least one character in letters is in self.s
        for e in letters:
            if e in self.s:
                return True
        return False

    def guessLanguage(self):  # Makes use of most common words in English and Turkish, stalemates are broken by checking language-specific letters (default: "tr").
        # Base case
        if len(self.s) < 1:
            return None
        # Defining stopwords for English and Turkish languages
        most_common_words_english = ["the", "be", "am", "is", "are", "was", "were", "to", "of", "and", "a", "in", "that", "have", "has", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "does", "did", "done", "at", "this", "but", "his", "by", "from", "they", "we", "say", "says", "said", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "gets", "got", "gotten", "which", "go", "goes", "went", "gone", "me", "when", "make", "makes", "made", "can", "like", "likes", "liked", "time", "no", "just", "him", "know", "knows", "knew", "known", "take", "takes", "took", "taken", "people", "into", "year", "your", "good", "some", "could", "them", "see", "sees", "saw", "seen", "other", "than", "then", "now", "look", "look", "looked", "only", "come", "comes", "came", "its", "over", "think", "thinks", "thought", "also", "back", "after", "use", "uses", "used", "two", "how", "our", "work", "works", "worked", "first", "well", "way", "even", "new", "want", "wants", "wanted", "because", "any", "these", "give", "gives", "gave", "given", "day", "most", "us"]
        most_common_words_turkish_speaking = ["bir", "bu", "ne", "ve", "mi", "için", "çok", "ben", "o", "de", "evet", "var", "ama", "mı", "değil", "da", "hayır", "sen", "şey", "daha", "bana", "kadar", "seni", "beni", "iyi", "tamam", "onu", "bunu", "gibi", "yok", "benim", "her", "sana", "ki", "sadece", "neden", "burada", "senin", "ya", "zaman", "hiç", "şimdi", "nasıl", "sonra", "olduğunu", "en", "mu", "misin", "hadi", "şu"]
        most_common_words_turkish_writing = ["ve", "bir", "olmak", "bu", "için", "da", "de", "etmek", "o", "ile", "çok", "daha", "gibi", "yapmak", "en", "ben", "bende", "bana", "beni", "ne", "var", "sonra", "her", "kadar", "kendi", "ama", "yıl", "insan", "almak", "ise", "ki", "içinde", "türkiye", "gelmek", "biz", "bizim", "bizde", "bize", "zaman", "iş", "iki", "değil", "büyük", "gün", "demek", "arasında", "yeni", "ilk", "önce", "vermek", "konu", "son", "iyi", "yok", "göre", "veya", "ancak", "şey", "taraf", "dünya", "başkan", "diye", "tüm", "aynı", "önemli", "karşı", "ilgili", "siz", "sizde", "sizi", "sizin", "gerekmek", "orta", "yer", "almak", "sadece", "hem", "şekilde", "diğer", "devam", "etmek", "sahip", "durum", "türk", "geçmek", "bile", "kişi", "hiç", "nasıl", "genel", "tek", "fazla", "ön", "birlikte", "böyle", "başka", "bütün", "devlet", "bulmak", "çünkü", "yani", "sen", "güzel", "yol", "eğitim", "an", "bin", "şu", "neden", "hal", "biri", "bazı"]
        # Filling the word array
        word_array = []
        temp_word = ""
        for i in range(0, len(self.s)):
            if self.s[i].isalnum() or self.s[i] in ["'", "-", "_", "/", "’"]:
                temp_word += self.s[i]
                if i == len(self.s) - 1:
                    if len(temp_word) > 0:
                        word_array.append(temp_word)
                        temp_word = ""
            else:
                if len(temp_word) > 0:
                    word_array.append(temp_word)
                    temp_word = ""
        # Analyzing word frequencies to compare
        english_count = 0
        turkish_count = 0
        for e in word_array:
            if e in most_common_words_english:
                english_count += 1
            elif e in most_common_words_turkish_speaking or e in most_common_words_turkish_writing:
                turkish_count += 1
        if english_count > turkish_count:
            return "en"
        elif english_count < turkish_count:
            return "tr"
        # Analyzing alphabet-specific occurrences to compare
        else:
            english_letters = ['x', 'X', 'q', 'Q', 'w', 'W']
            turkish_letters = ['ç', 'Ç', 'ğ', 'Ğ', 'ı', 'İ', 'ö', 'Ö', 'ş', 'Ş', 'ü', 'Ü']
            if self.anyInString(turkish_letters):
                return "tr"
            elif self.anyInString(english_letters):
                return "en"
            # Default value = "tr"
            else:
                return "tr"
