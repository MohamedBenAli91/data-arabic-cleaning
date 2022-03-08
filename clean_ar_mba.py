# coding=utf-8
# modifyed by Mohamed BEN ALI -- Data Scientist - Data Engineer  
# usage  python3 test.py -i <file_path> -o <output_file_result_path>
 


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
import sys
import argparse


arabic_punctuations = '''`https?://[A-Za-z./]*@[\w]*[^a-zA-Z#][a-zA-Z0-9][a-zA-Z0-9]|[:;]-?[()ODp][A-Z][a-z]+|\d+|[A-Z]+(?![a-z])^w^{<>_()*&^%][^`^l/:"^=.,'{}~+|!^`^}^`^`^|^`^s^`'''
english_punctuations = string.punctuation
latin_alphabic =  '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
num = '''0123456789'''
punctuations_list = arabic_punctuations + english_punctuations + latin_alphabic + num


arabic_diacritics = re.compile("""
                             ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
def clean(text):
    """
    This function cleans the text using the NLTK library.
    """
    stop_words = set(stopwords.words('arabic'))
    lemmatizer = WordNetLemmatizer()

    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


def normalize_arabic(text):
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    return text

def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text

def remove_symbols_from_text(text):
  symbols = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~https?://[A-Za-z./]*@[\w]*[^a-zA-Z#][a-zA-Z0-9][a-zA-Z0-9]|[:;]-?[()ODp][A-Z][a-z]+|\d+|[A-Z]+(?![a-z])'
  for symbol in symbols:
    text = text.replace(symbol, '')
  return text

def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)



def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)



parser = argparse.ArgumentParser(description='Pre-process arabic text (remove '
                                             'diacritics, punctuations, and repeating '
                                             'characters).')

parser.add_argument('-i', '--infile', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='input file.', required=True)
parser.add_argument('-o', '--outfile', type=argparse.FileType(mode='w', encoding='utf-8'),
                    help='out file.', required=True)


if __name__ == '__main__':
    args = parser.parse_args()
    text = args.infile.read()
    text = clean(text) 
    text = remove_symbols_from_text(text)
    text = remove_punctuations(text)
    text = remove_diacritics(text)
    text = remove_repeating_char(text)
    text = remove_emoji(text)
    args.outfile.write(text)

 
