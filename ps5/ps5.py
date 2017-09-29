# 6.00 Problem Set 5
# RSS Feed Filter
# Denis Savenkov
# ps5.py

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# MY CODE
# NewsStory
class NewsStory(object):

    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# MY CODE
# WordTrigger
class WordTrigger(Trigger):

    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        import re

        text = text.lower()
        text = re.split('\W+', text)

        return self.word.lower() in text

# TitleTrigger
class TitleTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_title())
    
# SubjectTrigger
class SubjectTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
    
# SummaryTrigger
class SummaryTrigger(WordTrigger):

    def __init__(self, word):
        WordTrigger.__init__(self, word)

    def evaluate(self, story):
        return self.is_word_in(story.get_summary())


# Composite Triggers
# Problems 6-8

# MY CODE
# NotTrigger
class NotTrigger(Trigger):

    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# AndTrigger
class AndTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) and\
               self.trigger2.evaluate(story)

# OrTrigger
class OrTrigger(Trigger):

    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return self.trigger1.evaluate(story) or\
               self.trigger2.evaluate(story)


# Phrase Trigger
# Question 9

# MY CODE
# PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return self.phrase in story.get_subject() or\
               self.phrase in story.get_title() or\
               self.phrase in story.get_summary()



#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # Problem 10

    # MY CODE
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
                break
            
    return filtered_stories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    # Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones

    # MY CODE
    trigger_list = []
    trigger_dic = {}
    for line in lines:
        line = line.split()
        if line[0] != 'ADD':
            name = line[0]
            if line[1] == 'TITLE':
                trigger_dic[name] = TitleTrigger(line[2])
            elif line[1] == 'SUBJECT':
                trigger_dic[name] = SubjectTrigger(line[2])
            elif line[1] == 'SUMMARY':
                trigger_dic[name] = SummaryTrigger(line[2])
            elif line[1] == 'NOT':
                trigger_dic[name] = NotTrigger(trigger_dic[line[2]])
            elif line[1] == 'AND':
                trigger_dic[name] = AndTrigger(trigger_dic[line[2]], trigger_dic[line[3]])
            elif line[1] == 'OR':
                trigger_dic[name] = OrTrigger(trigger_dic[line[2]], trigger_dic[line[3]])
            elif line[1] == 'PHRASE':
                phrase = ' '.join(line[2:])
                trigger_dic[name] = PhraseTrigger(phrase)
        else:
            for trigger in line[1:]:
                trigger_list.append(trigger_dic[trigger])

    return trigger_list
            
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")
    
    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

