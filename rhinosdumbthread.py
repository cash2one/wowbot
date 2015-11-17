import discord
import logging
import time
from random import randint
import praw
from threading import Thread

class timeThread(Thread):
    def __init__(self,time,discordid,discordpw,redditid,redditpw):
        Thread.__init__(self)
        #Real Timer self.timer = (time*60)+1
        self.timer = 10+1 #Fake Test Timer
        self.discordid = discordid
        self.discordpw = discordpw
        self.redditid = redditid
        self.redditpw = redditpw
        print('in timer')
    def run(self):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(filename='error.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)
        client = discord.Client()
        client.login(self.discordid,self.discordpw)
        if not client.is_logged_in:
            print('Login fail')
            exit(1)
        else:
            print('Connected on time thread!')
            print('Username: ' + client.user.name)
            print('ID: ' + client.user.id)
            print('--Server List--')
            for server in client.servers:
                print(server.name)
            
        while True:
            print(len(client.servers))
            for server in client.servers:
                print('in 1st for')
                if server.name == 'RhinoTest' and doit:
                    print('in server if')
                    for channel in server.channels:
                        print('in channel loop')
            #client.send_message(channel, 'REDDIT CONTENT!')
            # Sleep for random time between -10 and +10 defined minutes
            print('ding!')
            secondsToSleep = randint(self.timer-10, self.timer+10)
            print('%s sleeping timing thread for {} minutes...'.format(secondsToSleep/60))
            time.sleep(secondsToSleep)
        
