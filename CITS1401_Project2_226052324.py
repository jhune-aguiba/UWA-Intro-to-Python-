# Jhune Aguiba - 22605234
# CITS1401 - Project 2

import math

def calculateDistance(profile1, profile2): #calculates the distance between the 2 profiles
    differences = [ ]
    for key1 in profile1:
        if key1 in profile2:
            differences.append((abs(profile1[key1]) - (profile2[key1])))
        else:
            profile2[key1] = 0
            differences.append(profile1[key1])         
    for key2 in profile2:
        if key2 not in profile1:
            profile1[key2] = 0
            differences.append(profile2[key2]) 
            
    squared_differences = [ ]
    for difference in differences:
        squared_differences.append(difference**2)
        
    total_squared_differences = 0
    for squared in squared_differences:
        total_squared_differences += squared
        
    distance = 0
    distance = math.sqrt(total_squared_differences)
    return distance

def conjunctions(text): #returns count of required pieces of conjunction
    for ch in '.,""?!:;_@#$%^&*()=+[]{}\|<>/':
        text = text.replace(ch, ' ')
    words = text.split()
    conjunctionList = ["also", "although", "and", "as", "because", "before", "but",
                       "for", "if", "nor", "of", "or", "since", "that", "though",
                       "until", "when", "whenever", "whereas", "which", "while", "yet"]
    
    conjunction = dict((c,0) for c in conjunctionList)
    for word in words:
        if word in conjunction:
            conjunction[word] += 1
    return conjunction

def unigrams(text): #returns the count of each word
    for ch in '.,""?!:;_@#$%^&*()=+[]{}\|<>/':
        text = text.replace(ch, ' ')
    words = sorted(text.lower().split())
    
    unigram = {}
    for w in words:
        if w[0] == "'": #conditional statements deal with apostrophes that aren't contractions
            w = w[1:]
            unigram[w] = unigram.get(w, 0) + 1
        elif w[-1] == "'":
            w = w[:-1]
            unigram[w] = unigram.get(w, 0) + 1
        elif w != "'" or w != "":
            unigram[w] = unigram.get(w, 0) + 1
    return unigram

def punctuation(text): #returns count of required pieces of punctuation
    for ch in '"':
        text = text.replace(ch, ' ')
    words = text.split()
    punctuationList = [",", ";"]
    punctuations = dict((p,0) for p in punctuationList)
    for word in words:
        for ch in word:
            if ch in punctuationList:
                punctuations[ch] += 1

    apostrophe = {"'" : 0}
    for word in words:
            if len(word) >= 3:
                if word[-2] == "'" or word[-3] == "'":
                    apostrophe["'"] = apostrophe.get("'", 0) + 1
    punctuations.update(apostrophe)
    
    hyphen = {"-" : 0}
    for word in words:  
        if word.count("-") == 1:
            hyphen["-"] = hyphen.get("-", 0) + 1
        elif "-" in word != word[0] or "-" in word != word[1]:
            hyphen["-"] = hyphen.get("-", 0) + 1
    punctuations.update(hyphen)
             
    return punctuations

def words_per_sentence(text): #returns average number of words per sentence
    for ch in '?!':
        text = text.replace(ch, '.')
    sentences = text.split('.')
    sentences.pop(len(sentences)-1)
    totalNumofWords = text.split()
    average = len(totalNumofWords) / len(sentences)
    return average

def sentences_per_par(text): #returns average number of sentences per paragraph
    for ch in '?!':
        text = text.replace(ch, '.')
    totalSentences = text.split('.')
    totalSentences.pop(len(totalSentences)-1)
    pharagraphs = text.count("\n\n") + 1
    average = len(totalSentences) / pharagraphs
    return average

def composite(text):
    profile = { }
    profile.update(conjunctions(text))
    profile.update(punctuation(text))
    profile["words_per_sentence"] = round(words_per_sentence(text), 4)
    profile["sentences_per_par"] = round(sentences_per_par(text), 4)
    return profile

def main(filename1, filename2, feature): #opens the 2 files and calls required functions
    try:
        text1 = open(filename1, 'r').read()
        text2 = open(filename2, 'r').read()
        text1= text1.replace("--", " ").lower()
        text2= text2.replace("--", " ").lower()
    except:
        return None, None, None

    profile1 = { }
    profile2 = { }
    if feature == 'punctuation':
        profile1.update(punctuation(text1))
        profile2.update(punctuation(text2))
    elif feature == 'unigrams':
        profile1.update(unigrams(text1))
        profile2.update(unigrams(text2))
    elif feature == 'conjunctions':
        profile1.update(conjunctions(text1))
        profile2.update(conjunctions(text2))
    elif feature == 'composite':
        profile1.update(composite(text1))
        profile2.update(composite(text2))
    else:
        return None, None, None

    distance = round(calculateDistance(profile1, profile2), 4)
    
    return distance, profile1, profile2