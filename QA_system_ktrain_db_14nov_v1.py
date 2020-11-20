#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
{Question and Answering model: Run the script with mandatory parameters --> Company and Path}
{Example:python QA_system_ktrain_db_14nov_v1.py Edison "D:\Datasets\Question-Answer NLP\reports\Edison International\eix-2019-sustainability-repo
rt_mini.pdf"}
{prerequisites : python3.6+}
{steps: 1. Run qa_requirements.txt file 2. Execute Actual python script QA_system_ktrain_db_v1.py with two madatory parameters 'Company' and 'path'}
{Author: Dineshbabu}
{Date:14-Nov-20}
{Version: v1.3}

"""
# Package Imports

#Generic/Built-in
import os
import pandas as pd
import re
import nltk
from nltk import word_tokenize,sent_tokenize
import argparse

#other Libraries
import ktrain
from ktrain import text
from pdf_layout_scanner import layout_scanner

def text_cleaning(txt):
    '''This function would do text cleaning appropriate for multi-layout text extracted using pdf_layout_scanner library'''
    # txt = txt.strip()
    txt = re.sub(r'\b\w{,1}\b', '', txt)
    pattern = "\n{2,}"
    txt = re.sub(pattern, '*', txt)
    txt = re.sub("\n", " ", txt)
    txt = re.sub("\xa0", " ", txt)
    txt = re.sub("/*\d+\s+", "", txt)
    txt = txt.split('*')
    output = [l for l in txt if len(re.findall(r'\w+', l)) > 5]
    output = list(map(str.strip, output))
    return output

def text_extraction(path_to_file):
    '''This function would extract text from PDF using pdf_layout_scanner package'''
    listname = []
    pages = layout_scanner.get_pages(path_to_file)
    for i in range(len(pages)):
        listname += text_cleaning(pages[i])
    return listname


def get_answer (lstname,qn):
  '''This function would take question as input and return customized answers, backbone architecture is based on Transformer'''
  INDEXDIR =  '/tmp/myindex'
  try:
    text.SimpleQA.initialize_index(INDEXDIR)
  except :
    print ("\nIndex File already exists!! \n")
  # listname = cmp+'_list'
  # print (type(listname))
  text.SimpleQA.index_from_list(lstname, INDEXDIR, commit_every=len(lstname),multisegment=True, procs=4, breakup_docs=True)
  qa = text.SimpleQA(INDEXDIR)

  tokens = qn.lower().split()
  qn_words = ['are', 'does', 'have', 'can', 'am', 'is', 'was', 'were', 'do', 'did', 'has', 'could', 'should', 'may', ]
  # result =  [tokens[0] in [i for i in qn_words]]
  answers = qa.ask(qn)
  print ("\nActual Question : "+qn)
  print ("Answer : ")
  if ([tokens[0] in [i for i in qn_words]]) :
    if answers[0]['confidence'] >= 0.40:
      print("Yes, " + answers[0]['answer'])
    elif answers[0]['confidence'] < 0.40:
      print( "I guess, " + answers[0]['answer'])
  else:
    if answers[0]['confidence'] >= 0.40:
      print( answers[0]['answer'])
    elif answers[0]['confidence'] < 0.40:
      print( "I guess, " + answers[0]['answer'])

def ask_question():
    '''Recursive function to get Question as input'''

    question = input ("Please Ask you Question: ")
    if len(question) >= 10: # prevents empty question or questions with few words
        get_answer(gl_listname,question)
        repeat = input ("Do you want to ask more questions for the company, "+args.company+"[y/n] : ")
        if repeat.lower() == 'y':
            ask_question()
        else:
            print ("Thank you!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My example explanation')
    parser.add_argument('company', type=str, help="Enter company name in camel caps. Eg: Edison")
    parser.add_argument('path', type=str, help="Enter pdf file path")
    args = parser.parse_args()
    print(f"Company: {args.company} \n Path:{args.path}")
    # global qn_words
    # text_extraction(args.path)
    # listname = args.company+'_list'
    # global gl_listname
    gl_listname = text_extraction(args.path)
    ask_question()
    ###        End of Main       ###


