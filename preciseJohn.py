#!/usr/share/python

import sys, os, re, subprocess, argparse

def main(argv):
    args = getArguments()
    beginCrack(args.wordlist, args.passwordfile)

def getArguments():
    parser = argparse.ArgumentParser(prefix_chars='-')

    parser.add_argument('-w', '--wordlist', help='Passwords dictionary', required=True)
    parser.add_argument('-p', '--passwordfile', type=str, help='Password file to crack', required=True)

    args = parser.parse_args()

    return args

def beginCrack(wordlist, passwordfile):
    possibleHashes = getPossibleHashes(passwordfile)
    startJohn(wordlist, passwordfile, possibleHashes)

def getPossibleHashes(passwordfile):
    command = "john --list=formats | tr --delete \"\n\""
    johnFormats = subprocess.getoutput(command)
    johnFormats = johnFormats.split(", ")

    command = "hashid " + passwordfile + " -j"
    possibleJohnFormats = subprocess.getoutput(command)
    possibleJohnFormats = possibleJohnFormats.split("\n")

    possibleHashes = list()

    for johnFormat in johnFormats:
        for possibleJohnFormat in possibleJohnFormats:
            regex = "[^a-zA-Z0-9]" + johnFormat.lower() + "[^a-zA-Z0-9]"
            if re.search(regex, possibleJohnFormat.lower()):
                possibleHashes.append(johnFormat)

    possibleHashes = list(dict.fromkeys(possibleHashes))
    print("Hashes found:")
    print(possibleHashes)
    print("\n")

    return possibleHashes

def startJohn(wordlist, passwordfile, possibleJohnFormatsList):
    for format in possibleJohnFormatsList:
        print("Trying " + format + " format on " + passwordfile + " file.")
        print("Using " + wordlist + " dictionary.")
        
        command = "john --format=" + str(format) + " --wordlist=" + wordlist + " " + passwordfile
        os.system(command)

        print("\n")

if __name__ == "__main__":
    main(sys.argv[1:])
