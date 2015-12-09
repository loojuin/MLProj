# -*- coding: utf-8 -*-
"""
Created on Tue Dec 08 22:12:34 2015

@author: Rama
"""

def wordsorter(word):
    if word[0]=="@":
        return "@user"
    elif word[:4]=="http":
        return "http://<url>"
    elif word[0]=="#":
        return "#hashtag"
    else:
        return word
        
if __name__ == "__main__":
    word1="@riqshaa"
    word2="http:/facebook.com"
    word3="#money"
    word4="pussy"
    print wordsorter(word4)