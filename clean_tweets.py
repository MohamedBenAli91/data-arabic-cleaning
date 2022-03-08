# coding=utf-8
# clean_tweets.py by Mohamed BEN ALI -- Data Scientist - Data Engineer  
# usage  python3 clean_ar1.py -i <file_path> -o <output_file_result_path>
 

import re
import string
import sys
import argparse

arabic_punctuations = '''`         ^w   ^{<>_()*&^%][   ^`   ^l/:"   ^=.,'{}~      +|!   ^`^}   ^`      ^  @[\w]*  https?://[A-Za-z./]*  [^a-zA-Z#] [a-zA-Z0-9]  [a-zA-Z0-9]|[:;]-?[()ODp] 
[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])  `^|   ^`^s   ^`'''
english_punctuations = string.punctuation + string.digits
latin_alphabic =  '''`     a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L  M N O P Q R S T U V W X Y Z `'''
punctuations_list = arabic_punctuations + english_punctuations +  latin_alphabic 

arabic_diacritics = re.compile("""
                                ^q    | # Tashdid
                                ^n    | # Fatha
                                ^k    | # Tanwin Fath
                                ^o    | # Damma
                                ^l    | # Tanwin Damm
                                ^p    | # Kasra
                                ^m    | # Tanwin Kasr
                                ^r    | # Sukun
                                ^`     # Tatwil/Kashida
                         """, re.VERBOSE)


def normalize_arabic(text):
    text = re.sub("[                        ]", "      ", text)
    text = re.sub("   ^i", "   ^j", text)
    text = re.sub("      ", "      ", text)
    text = re.sub("      ", "      ", text)
    text = re.sub("      ", "   ^g", text)
    text = re.sub("      ", "   ^c", text)
    return text


def remove_diacritics(text):
    text = re.sub(arabic_diacritics, '', text)
    return text


def remove_punctuations(text):
    translator = str.maketrans('', '', punctuations_list)
    return text.translate(translator)


def remove_repeating_char(text):
    return re.sub(r'(.)\1+', r'\1', text)



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
    text = remove_punctuations(text)
    text = remove_diacritics(text)
    text = remove_repeating_char(text)
    args.outfile.write(text)

