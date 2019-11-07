import re #import to remove non-alphabetic characters
import os #import to clear screen
import time #import to measure time
import datetime #import to measure date

from difflib import SequenceMatcher #import to possibly change a wrong word, check simmilarity between words

def remove_endspacetext(text): #function to remove every endspace in a string
    if '\n' in text:
        text = text.replace("\n"," ")
    return text

with open("EnglishWords.txt") as file: #open the dictionary and read it in a list
    englishwords = file.readlines()

englishwords = [line.rstrip('\n') for line in open("EnglishWords.txt")] #remove every endspace in the EnglishWords text file and put the result in the englishwords list

sentence = ""

while True:
    os.system("clear") #this command clears the screen for a better view and menu for the programme
    selection = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503    S P E L L   C H E C K E R        \u2503
    \u2503                                     \u2503
    \u2503        1. Check a file              \u2503
    \u2503        2. Check a sentence          \u2503
    \u2503                                     \u2503
    \u2503        0. Quit                      \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Enter choice: """) #asks the user whether they want to check a file or a sentence
    os.system("clear")
    if selection not in ["1","2","0"]: #makes sure the input is 1, 2 or 0 and proceeds accordingly
        continue
    elif selection == "0":
        exit()

    elif selection == "1": #if the user wants to check a file:
        fileselect = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503    L O A D  F I L E                 \u2503
    \u2503                                     \u2503
    \u2503        Enter the file name          \u2503
    \u2503        then press [enter]           \u2503
    \u2503                                     \u2503
    \u2503                                     \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Filename: """)
        try:                           #tries to see if the file can be found
            with open(fileselect) as file:   #open the file, remove all unwanted characters and put the whole txt file in the sentence list
                sentence = file.read()
                sentence = remove_endspacetext(sentence)
                sentence = re.sub('[^a-zA-Z ]', "", sentence)
                sentence = [word for word in sentence.split(" ") if word!='']
        except FileNotFoundError:
            continue

    elif selection == "2": #if the user wants to check a sentence:
        sentence = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503    E N T E R  S E N T E N C E       \u2503
    \u2503                                     \u2503
    \u2503         Enter sentence              \u2503
    \u2503          to spellcheck              \u2503
    \u2503                                     \u2503
    \u2503                                     \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Sentence: """)
        sentence = re.sub('[^a-zA-Z ]', "", sentence)
        sentence = sentence.split() #lets the user enter the sentence, removes any character that is not in the alphabet and puts the sentence in a list

    correctnr, incorrectnr, ignored_nr, marked_nr, addedtodict_nr, changed_counter, run_writeinenglist = 0, 0, 0, 0, 0, 0, 0
    sentence_rewrite = ""

    time_start = time.time_ns() #starts measuring the time

    for i in range (len(sentence)):
        os.system("clear")
        if sentence[i].casefold() in englishwords: #checks to see if the word in the sentence is in the english words dictionary
            sentence_rewrite = sentence_rewrite + sentence[i] + " "
            correctnr = correctnr + 1
        else: #else tries to search for an approrpiate replacement suggestion, with SequenceMatcher, for any word not found in the dictionary
            biggest_score = 0.0
            possible_word = ""
            for test_word in englishwords:
                score = SequenceMatcher(None,sentence[i].casefold(),test_word).ratio()
                if score > biggest_score: #the word with the biggest score will be picked
                    biggest_score = score
                    possible_word = test_word
            changeword_choice = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503       C H A N G E  W O R D ?        \u2503
    \u2503      You entered:                   \u2503
    \u2503       {0}{1}\u2503
    \u2503      Did you mean:                  \u2503
    \u2503       {2}{3}\u2503
    \u2503      Enter y/yes or n/no            \u2503
    \u2503      (or any other key for no)      \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Enter choice: """.format(str(sentence[i]),''.join([" " for i in range(30-len(sentence[i]))]), possible_word, ''.join([" " for i in range(30-len(possible_word))])))
            #after finding the word, asks the user if they want to change it
            if changeword_choice in ["y","Y","yes","Yes"]:
                sentence_rewrite = sentence_rewrite + possible_word + " "
                changed_counter = changed_counter + 1
                incorrectnr = incorrectnr + 1
                continue
            os.system("clear")
            while True: #if they do not want to change it, asks the user what they want to do with the word:
                word_choice = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503    W O R D  N O T  F O U N D        \u2503
    \u2503       {0}{1}\u2503
    \u2503                                     \u2503
    \u2503    1. Ignore the word               \u2503
    \u2503    2. Mark the word as incorrect.   \u2503
    \u2503    3. Add word to dictionary.       \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Enter choice: """.format(str(sentence[i]),''.join([" " for i in range(30-len(sentence[i]))])))
                if word_choice not in ["1","2","3"]:
                    os.system("clear")
                    continue
                if word_choice == "1": #ignore the word
                    sentence_rewrite = sentence_rewrite + "!" + sentence[i] + "! "
                    ignored_nr = ignored_nr + 1
                    incorrectnr = incorrectnr + 1
                elif word_choice == "2": #mark the word as incorrect
                    sentence_rewrite = sentence_rewrite + "?" + sentence[i] + "? "
                    marked_nr = marked_nr + 1
                    incorrectnr = incorrectnr + 1
                elif word_choice == "3": #write the word in the dictionary
                    sentence_rewrite = sentence_rewrite + "*" + sentence[i] + "* "
                    addedtodict_nr = addedtodict_nr + 1
                    incorrectnr = incorrectnr + 1
                    englishwords.append(sentence[i])
                    englishwords.sort()
                    run_writeinenglist = 1
                break

    time_taken = (time.time_ns() - time_start) // 1000 #takes the time taken

    details_output="""\n   Number of words: {0}
   Number of correctly spelt words: {1}
   Number of incorrectly spelt words: {2}
    Number ignored: {3}
    Number marked: {4}
    Number added to dictionary: {5}
   Number of changed words: {6}
    """.format(len(sentence),correctnr,incorrectnr,ignored_nr,marked_nr,addedtodict_nr,changed_counter)
    os.system("clear")
    print (details_output)
    print ("    Time elapsed " + str(time_taken) + " microseconds\n") #displays the data about the words and the time it took for the programme to run

    if selection == "1": #if the user checked a file, rewrite the corrected file with the date and time, the data about the words and the corrected sentence
        with open("correct_" + fileselect, "w") as file:
            file.write(str(datetime.datetime.now()) + "\n" + details_output + "\n" + sentence_rewrite)

    elif selection == "2": #if the user checked a sentence, display just the corrected sentence
        print (" Your corrected text is: " + sentence_rewrite + "\n")

    if run_writeinenglist == 1: #if the user decided to write anything in the dictionary, run this conditional and rewrite the dictionary with the words the user decided to add ti dictionary
        with open ("EnglishWords.txt","w") as file:
            new_englishwords = ""
            for new_word in englishwords:
                new_englishwords = new_englishwords + new_word + "\n"
            file.write(new_englishwords)

    sentence = ""
    anothergame = input("""
    \u250F\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2513
    \u2503             R E - R U N             \u2503
    \u2503                                     \u2503
    \u2503     Press q [enter] to quit or      \u2503
    \u2503                                     \u2503
    \u2503  any other key [enter] to go again  \u2503
    \u2503                                     \u2503
    \u2523\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u251B
    \u2517\u2501\u2501\u2501\u2501 Enter choice: """) #asks the user if they want to run the programme again
    if anothergame in {"q","Q","0"}:
        os.system("clear")
        break
