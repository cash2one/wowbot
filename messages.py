import discord
import logging
import time
import random
import praw
from threading import Thread

class msgThread(Thread):
    def __init__(self,discordid,discordpw,redditid,redditpw):
    
        Thread.__init__(self)
        self.discordid = discordid
        self.discordpw = discordpw
        self.redditid = redditid
        self.redditpw = redditpw
        
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
        
        with open('quotes.txt') as f:
            quotes = f.readlines()
        with open('helpmessage.txt') as f:
            helpmessage = f.read()
        roles = [f.strip() for f in open('roles.txt')]
        f.close()
        lockroles = ["Moderator", "Chat Moderator", "Twitterbot"]
        cannotset = """Sorry I could not set your class because I did not
                    recognize the class you chose. Type `@WoWbot help` for
                    more information."""
        @client.event
        def on_ready():
            print('Connected on messages thread!')
            print('Username: ' + client.user.name)
            print('ID: ' + client.user.id)
            print('--Server List--')
            for server in client.servers:
                print(server.name)
        
        
        @client.event
        def on_message(message):
            for people in message.mentions:
                if people.name == client.user.name :
                    if 'help' in message.content.lower():
                        client.send_message(message.channel, helpmessage)
                        
                    elif 'class' in message.content.lower():
                        doit = True
                        for role in message.author.roles:
                            if role.name in lockroles:
                                  doit = False
                        if 'remove' in message.content.lower() and doit and len(message.author.roles) != 0:
                            client.replace_roles(message.author,client.servers[1].roles[0])
                            break
                        try:
                            myrole = next(role for role in roles if role in message.content.lower().split())
                        except:
                            myrole = "unrecognized"
                            doit = False
                            client.send_message(message.author, cannotset)
                        print('setting ' + message.author.name + ' as ' + myrole)
                        for server in client.servers:
                            print('in 1st for')
                            if server.name == 'RhinoTest' and doit:
                                print('in server if')
                                for role in server.roles:
                                    print('in role loop')
                                    if (myrole == role.name.lower() and len(message.author.roles) != 0):
                                        print('trying with existing role')
                                        client.replace_roles(message.author,role)
                                    elif (myrole == role.name.lower()):
                                        print('trying with no prev roles')
                                        client.add_roles(message.author,role)


                    elif 'rickme' in message.content.lower():
                        client.send_message(message.channel, random.choice(quotes))
        client.run()
