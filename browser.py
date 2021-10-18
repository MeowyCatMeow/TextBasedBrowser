"""
Text Based Browser
https://hyperskill.org/projects/79/stages/441/implement
https://imgur.com/5AQ13Ke
"""
import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class TextBasedBrowser:
    def __init__(self):
        self.path = sys.argv[1]
        self.choice = ''
        self.txt_name = ''
        self.history_stack = deque()

    def save_file(self, link):
        try:
            r = requests.get(link)
        except requests.exceptions.ConnectionError:
            print('Error: Incorrect URL')
            return
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            paragraphs = soup.get_text()
            paras = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "a", "ul", "ol", "li"])
            for i in paras:
                if 'a' in str(i):
                    print(Fore.BLUE + i.get_text())
                else:
                    print(i.get_text())
            with open(self.txt_name, 'w', encoding='utf-8') as f:
                f.writelines(paragraphs)

    def back(self):
        try:
            self.history_stack.pop()
            print(self.history_stack.pop())
        except IndexError:
            print('No browser history')

    def actions(self):
        while True:
            self.choice = input()
            if '.' in self.choice:
                self.txt_name = self.choice.split('.')[0]
                self.choice = ('https://' + self.choice) if 'https://' not in self.choice else self.choice
                # print(self.choice)
                self.save_file(self.choice)
                self.history_stack.append(self.choice)
            elif self.choice == 'back':
                self.back()
            elif self.choice == 'exit':
                exit()
            else:
                print('Error: Incorrect URL')

    def operate(self):
        if os.access(self.path, os.F_OK) is False:
            os.mkdir(self.path)
        os.chdir(self.path)
        self.actions()


txt = TextBasedBrowser()
txt.operate()
