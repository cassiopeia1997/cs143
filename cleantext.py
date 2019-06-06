#!/usr/bin/env python3

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse
import sys
import argparse
import json


__author__ = ""
__email__ = ""

# Depending on your implementation,
# this data may or may not be useful.
# Many students last year found it redundant.
_CONTRACTIONS = {
    "tis": "'tis",
    "aint": "ain't",
    "amnt": "amn't",
    "arent": "aren't",
    "cant": "can't",
    "couldve": "could've",
    "couldnt": "couldn't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "dont": "don't",
    "hadnt": "hadn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "hed": "he'd",
    "hell": "he'll",
    "hes": "he's",
    "howd": "how'd",
    "howll": "how'll",
    "hows": "how's",
    "id": "i'd",
    "ill": "i'll",
    "im": "i'm",
    "ive": "i've",
    "isnt": "isn't",
    "itd": "it'd",
    "itll": "it'll",
    "its": "it's",
    "mightnt": "mightn't",
    "mightve": "might've",
    "mustnt": "mustn't",
    "mustve": "must've",
    "neednt": "needn't",
    "oclock": "o'clock",
    "ol": "'ol",
    "oughtnt": "oughtn't",
    "shant": "shan't",
    "shed": "she'd",
    "shell": "she'll",
    "shes": "she's",
    "shouldve": "should've",
    "shouldnt": "shouldn't",
    "somebodys": "somebody's",
    "someones": "someone's",
    "somethings": "something's",
    "thatll": "that'll",
    "thats": "that's",
    "thatd": "that'd",
    "thered": "there'd",
    "therere": "there're",
    "theres": "there's",
    "theyd": "they'd",
    "theyll": "they'll",
    "theyre": "they're",
    "theyve": "they've",
    "wasnt": "wasn't",
    "wed": "we'd",
    "wedve": "wed've",
    "well": "we'll",
    "were": "we're",
    "weve": "we've",
    "werent": "weren't",
    "whatd": "what'd",
    "whatll": "what'll",
    "whatre": "what're",
    "whats": "what's",
    "whatve": "what've",
    "whens": "when's",
    "whered": "where'd",
    "wheres": "where's",
    "whereve": "where've",
    "whod": "who'd",
    "whodve": "whod've",
    "wholl": "who'll",
    "whore": "who're",
    "whos": "who's",
    "whove": "who've",
    "whyd": "why'd",
    "whyre": "why're",
    "whys": "why's",
    "wont": "won't",
    "wouldve": "would've",
    "wouldnt": "wouldn't",
    "yall": "y'all",
    "youd": "you'd",
    "youll": "you'll",
    "youre": "you're",
    "youve": "you've"
}

# You may need to write regular expressions.
# remove new line and tab
space_and_tab= re.compile(r'[\t\n ]+')
# remove url
url_remover=re.compile(r'https?:\/\/[^ ]*|www\.[^ ]')
#mark_link_remover=re.compile(r'\[.*\]\(\/r\/[^\)]*\)')
#external punctuation matching
punctuation_matcher = re.compile(r'([?.,:;!])')
# letter or number
#special_punctuation_matcher = re.compile(r'[][\@\#\&\|\^\*\+\|\/\\]')
#\#\&\|\^\*\+\|\/\\

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings 
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    # YOUR CODE GOES BELOW:
    
    parsed_text=space_and_tab.sub(' ',text)
    parsed_text=url_remover.sub('',parsed_text)
    
    #parsed_text=mark_link_remover.sub('',parsed_text)
    total=len(parsed_text)
    pos=[]
    i=0
    met1=False
    met2=False
    while (i<total):
        if(parsed_text[i]=='['):
            next=parsed_text.find(']',i)
            if(next!=-1):
                if(parsed_text[next+1]=='('):
                    next2=parsed_text.find(')',next+1)
                    if(next2!=-1):
                        pos.append(i)
                        pos.append(next)
                        pos.append(next+1)
                        pos.append(next2)
        i+=1

        #print(pos)
        #print(parsed_text)
    i=0
    result=""
    if(len(pos)>0):
    
        while(i<len(pos)):
            if(i>0):
                result+=parsed_text[pos[i-1]+1:pos[i]]+parsed_text[pos[i]+1:pos[i+1]]
            else:
                result+=parsed_text[:pos[i]]+parsed_text[pos[i]+1:pos[i+1]]
            i+=4
        parsed_text=result
    # separate all external punctuation
    result=""
    inside=False
    for ch in parsed_text:
        if punctuation_matcher.match(ch) and not inside:
            result+=" "+ch+" "
            inside=False
        else:
            if space_and_tab.match(ch):
                inside=False
            else:
                inside=True
            result+=ch
    #print(result)
    result=result[::-1]
    #print(result)
    inside=False
    result2=""
    for ch in result:
        if punctuation_matcher.match(ch) and not inside:
            result2+=" "+ch+" "
            inside=False
        else:
            if space_and_tab.match(ch):
                inside=False
            else:
                inside=True
            result2+=ch
    parsed_text=result2[::-1]

    parsed_text=space_and_tab.sub(' ',parsed_text)
    allwords = parsed_text.split(' ')
    i = 0

    while i < len(allwords):
        t = ""
        if allwords[i] in _CONTRACTIONS.values():
            i+=1
            continue
        else:
            for ch in allwords[i]:
                #print(ch)
                if ch in ['\\','#','&','|','^','*','+','|','/']:
                    #,'&','|','^','*','+','|','/','\'
                    t+=''
                else:
                    t+=ch
            allwords[i]=t
           
        
        i += 1
    parsed_text = ' '.join(allwords)

    parsed_text=parsed_text.lower()
    parsed_text=space_and_tab.sub(' ',parsed_text).strip()
    tokens = parsed_text.split(' ')
    tokens = list(filter(None, tokens))
    n = len(tokens)
    unigrams = []
    for i in range(n):
        if not punctuation_matcher.match(tokens[i]):
            unigrams.append(tokens[i])
    unigrams = ' '.join(unigrams)
    bigrams=[]
    for i in range(n-1):
        if not punctuation_matcher.match(tokens[i]) and not punctuation_matcher.match(tokens[i+1]):
            bigrams.append(tokens[i]+"_"+tokens[i+1])
    bigrams = ' '.join(bigrams)
    trigrams=[]
    for i in range(n-2):
        if not punctuation_matcher.match(tokens[i]) and not punctuation_matcher.match(tokens[i+1]) and not punctuation_matcher.match(tokens[i+2]):
            trigrams.append(tokens[i]+"_"+tokens[i+1]+"_"+tokens[i+2])
    trigrams = ' '.join(trigrams)
    return [parsed_text, unigrams, bigrams, trigrams]



if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.

    # YOUR CODE GOES BELOW.

    # We are "requiring" your write a main function so you can
    # debug your code. It will not be graded.
    #printAll(sanitize("I'm afraid I can't explain myself, sir. Because I am not myself, you see?"))
  
    filename=sys.argv[1]
    print(filename)
#except(Exception):
#       print("Problem when reading")
    with open(filename) as f:
        lines=f.readlines()
        lines=[x.strip() for x in lines]
        for line in lines:
            body=json.loads(line)["body"]
            result=sanitize(body)
            for l in result:
                print(l)

