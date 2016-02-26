import asyncio
import discord

from wowbot.constants import helpmsg, lockroles, cannotset


class WoWBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.prefix = '!'
        self.email = 'email'
        self.password = 'password'

    # noinspection PyMethodOverriding
    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start(self.email, self.password))
            loop.run_until_complete(self.connect())
        except Exception:
            loop.run_until_complete(self.close())
        finally:
            loop.close()

    async def on_ready(self):

        print('Connected!\n')
        print('Username: ' + self.user.name)
        print('ID: ' + self.user.id)
        print('--Server List--')
        for server in self.servers:
            print(server.name)

    async def timed_message(self, channel, message_content):
        timedmsg = await self.send_message(channel, message_content)
        await asyncio.sleep(15)
        await self.delete_message(timedmsg)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.strip().startswith(self.prefix):
            try:
                command, args = message.content.strip().split(None, 1)
            except:
                command = message.content.strip()
                pass

            if command in [self.prefix + 'help']:
                await self.delete_message(message)
                final_role_names = ''
                for role_to_check in message.server.roles:
                    if role_to_check.name not in lockroles and not role_to_check.is_everyone:
                        final_role_names += '{}, '.format(role_to_check.name)
                final_role_names = final_role_names[:len(final_role_names)-2]
                await self.timed_message(message.channel, helpmsg.format(self.prefix, final_role_names))

            elif command in [self.prefix + 'kill']:
                if message.author.id == '113097494489006080':
                    await self.logout()

            elif command in [self.prefix + 'clear']:
                is_mod = False
                author_roles = message.author.roles

                for role_to_check in author_roles:
                    if role_to_check.name in lockroles:
                        is_mod = True

                if is_mod:
                    for roles in message.author.roles:
                        if roles.name not in lockroles and not roles.is_everyone:
                            author_roles.remove(roles)
                    print('removing roles from mod {}'.format(message.author.name))
                    await self.replace_roles(message.author, *author_roles)
                else:
                    print('removing roles from user {}'.format(message.author.name))
                    self.replace_roles(message.author, message.server.default_role)
                await self.delete_message(message)
                await self.timed_message(message.channel, '<@{}>, I\'ve removed all classes from you!'
                                                          ''.format(message.author.id))

            elif command in [self.prefix + 'class']:
                if not args:
                    await self.timed_message(message.channel, cannotset)
                    return

                rolename = args
                role = discord.utils.get(message.server.roles, name=rolename)

                if not role:
                    await self.timed_message(message.channel, cannotset)
                    return

                if role.name in lockroles:
                    await self.timed_message(message.channel, cannotset)
                    return

                is_mod = False
                author_roles = message.author.roles
                for role_to_check in author_roles:
                    if role_to_check.name in lockroles:
                        is_mod = True

                if is_mod:
                    for roles in message.author.roles:
                        if roles.name not in lockroles and not roles.is_everyone:
                            author_roles.remove(roles)
                    author_roles.append(role)
                    print('giving role {} to mod {}'.format(role.name, message.author.name))
                    await self.replace_roles(message.author, *author_roles)
                else:
                    print('giving role {} to user {}'.format(role.name, message.author.name))
                    await self.replace_roles(message.author, role)
                await self.delete_message(message)
                await self.timed_message(message.channel,
                                         '<@{}>, you now are marked with the class `{}`!'.format(message.author.id,
                                                                                                 role.name))

if __name__ == '__main__':
    bot = WoWBot()
    bot.run()
