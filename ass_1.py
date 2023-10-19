import argparse
import os
import time
import string

from loguru import logger


import urllib.request
import matplotlib.pyplot as plt

# Sostituisci con il tuo URL
# https://www.gutenberg.org/cache/epub/1497/pg1497.txt
# https://www.gutenberg.org/files/71727/71727-0.txt

# Apri l'URL e leggi il contenuto


parser = argparse.ArgumentParser (prog='Lettercount',
                                  description='Counts the relative frequencies of the letters and other functions')

parser.add_argument ('infile', type=str, help="input the path file you wanna use")
parser.add_argument ('--l', '--light', help='Count the book text only, leave out everything else is not the book')
parser.add_argument ('--p', '--plot', help='plot an histogram of the relative frequencies')
parser.add_argument ('--b', '--base',
                     help='display the basic characteristics of the book: number of characters, number of words, number of lines')
parser.add_argument ('--count', help='count the relative frequencies of the alphabet letters')

alpha = list(string.ascii_lowercase)



def download(url):
    """
    
    Parameters url
    ----------
    url: stringa con l'url del file di testo da scaricare

    Returns: file di testo o Nan se file inesistente
    -------

    """

    try:
        with urllib.request.urlopen(url) as u:
            return u.read()
    except urllib.error.URLError as e:
        logger.error (f"Error accessing URL: {str (url)}")
        return "NaN"


def light_version(t_s): # Verificare che la variabile text sia oppure no un a stringa e stampare il testo in versione light
    
    c_1 = False
    index_controll = 0
    index_begin = 0
    for i in range(len(t_s)):
        
        if c_1 and (t_s[i] + t_s[i + 1] + t_s[i + 2] == '***'):
            index_controll = i + 2
            break
        if (t_s[i] + t_s[i+1] + t_s[i+2]) == '***':
            c_1 = True
            index_begin = i
       

    logger.info(f"The index of starting is {index_controll}")
    logger.info(f"the title is {text[index_begin+3:index_controll-2]}")
    return text[index_controll+1:]


def upload_dict(dict, key):
    if key in dict:
        a = dict[key] + 1
        dizionario.update ({key: a})
    return dict


def init_dict(keystring):
    """

    Parameters: string
    ----------
    keystring: the string of keys

    Returns: the initialized dictionary with the strinkeys ad keys
    -------

    """
    dict = {}
    for key in keystring:
        dict.update ({key: 0.0})
    return dict


def count(text):
    
    c= 0
    l = []
    dict = init_dict (alpha)
    logger.info ("Comincio il conteggio delle lettere")
    for carattere in text:
        qkey = carattere.lower ()

        if qkey in alpha:
            dict[qkey] += 1.
            c = c +1
   
    logger.info ("FINITO!!")
    for i in list(dict.values()): l.append(float(i)/c)
    return l


def basic(text):# VERIFICA CHE LA FUNZIONE SPLIT FUNZIONA COME TI ASPETTI

    # number of characters, number of words, number of lines
    n_w = text.count(' ')  # number of words
    n_l = text.count('\\r\\n')  # number of lines
    n_c = len(text) - n_w - n_l # number of characters
    
    print("In the text analysed there are:\n {} characters \n {} words \n {} lines".format (n_c, n_w, n_l))




def controller(text, args):
    """
    
    Parameters text commands
    ----------
    text: testo da analizzare
    args: insieme dei comandi dati da tastiera

    Returns: none
    -------

    """
    
    try:

        if args.l == 'L':
            logger.info ('You have set the light version')
            text = light_version(text)
            
            
        
        if args.count == 'COUNT':
            logger.info('We are counting the letters relative frequencies')
            freq_list = count(text)
            

        
        if args.b == 'B':
            logger.info('We are looking for the basics of the text')
            basic(text)
            
        

        if args.p == 'P':
            logger.info('We are plotting the histogram of the relative frequencies')
            
            plt.bar(alpha,freq_list)
            plt.savefig("mygraph.png")
            

    except:
        logger.error('CONTROLLER ERROR')




if __name__ == '__main__':
    args = parser.parse_args ()
    start_time = time.time ()
    text = str(download(args.infile))
    logger.info(f"{args.infile} downloaded")
    
    
    
    controller(text, args)

    elapsed_time = time.time () - start_time
    print(f"Total elapsed time: {elapsed_time}")
