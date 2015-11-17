#!/opt/python3.3/bin/python
import discord
import logging
import time
import random
import praw
from messages import msgThread 
from rhinosdumbthread import timeThread

try:
    import creds
except:
    print("Need valid creds.py to login")
    exit()

timerthread = timeThread(60,creds.discordid,creds.discordpw,creds.redditid,creds.redditpw)
messagesthread = msgThread(creds.discordid,creds.discordpw,creds.redditid,creds.redditpw)

timerthread.start()
messagesthread.start()
