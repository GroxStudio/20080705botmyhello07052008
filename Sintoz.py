import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import os

bot = commands.Bot(command_prefix='s.') #инициализируем бота с префиксом 's.'

#повторение сообщения
@bot.command(pass_context=True) #разрешаем передавать агрументы
@commands.has_permissions(administrator= True)
async def text(ctx, *, arg): #создаем асинхронную фунцию бота
    await ctx.send(arg) #отправляем обратно аргумент

#очистка чата
@bot.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)



#голосование с эмодзи
@bot.command(aliases=['голосование'])
@commands.has_permissions(administrator= True)
async def vote(ctx, *, arg):
    msg = await ctx.channel.send(embed = discord.Embed(description = f'**Голосование за:** {arg}'))
    await msg.add_reaction('🟢')
    await msg.add_reaction('🔴')
    await asyncio.sleep(1800)
    msg = await ctx.channel.fetch_message(msg.id)
    await ctx.channel.send(embed = discord.Embed(description = f"**За:** ``{[r for r in msg.reactions if r.emoji == '🟢'][0].count - 1}`` **Против:** ``{[r for r in msg.reactions if r.emoji == '🔴'][0].count - 1}``"))









#avatar preson
@bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'Аватар пользователя {user}', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)








#mute
@bot.command()
@commands.has_permissions(kick_members = True)
async def mute(ctx,*,member:discord.Member):
        author = ctx.message.author
        role = get( ctx.guild.roles, name = "muted")
        await member.add_roles(role)
        await ctx.send(f"участник {member.mention} больше не сможет говорить ")
        print("{0} замутил пользователя {1}".format(author,member))

@bot.command()
@commands.has_permissions(kick_members = True)
async def unmute(ctx,*,member:discord.Member):
        role = get(ctx.guild.roles,name = "muted")
        await member.remove_roles(role)
        await ctx.send(f"участник {member.mention} может снова говорить теперь")
        author = ctx.message.author
        print("{0} убрал мут с пользователя {1}".format(author,member))








#person-join
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(709403069871554591)
    guild = bot.get_guild(709053145497731172)
    role = discord.utils.get(guild.roles,id = 709137963690229840)
    await channel.send(" {0} Привет, добро пожаловать на наш сервер! Удачи в общении)! ".format(member.mention))
    await member.add_roles(role)






#logs
@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(709428447499255949)
    if message.content is None:
        return;
    embed = discord.Embed(colour=0xff0000, description=f"**{message.author} Удалил сообщение в канале {message.channel}** \n{message.content}",timestamp=message.created_at)

    embed.set_author(name=f"{message.author}", icon_url=f'{message.author.avatar_url}')
    embed.set_footer(text=f'ID Пользователя: {message.author.id} | ID Сообщения: {message.id}')
    await channel.send(embed=embed)
    return


#info2
@bot.command()
async def server(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"Сервер `{ctx.guild.name}`", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f":flag_white: **Регион: `{ctx.guild.region}`**\n\n"
        f":cowboy:  **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f":tools: **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f":green_circle: **Онлайн: `{online}`**\n\n"
        f":black_circle: **Оффлайн: `{offline}`**\n\n"
        f":yellow_circle: **Отошли: `{idle}`**\n\n"
        f":red_circle: **Не трогать: `{dnd}`**\n\n"
        f":shield: **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f":musical_keyboard: **Всего каналов: `{allchannels}`**\n\n"
        f":loud_sound: **Голосовых каналов: `{allvoice}`**\n\n"
        f":keyboard: **Текстовых каналов: `{alltext}`**\n\n"
        f":briefcase: **Всего ролей: `{allroles}`**\n\n"
        f":slight_smile: **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: {ctx.guild.name}")
    await ctx.send(embed=embed)








#гугл
@bot.command()
async def google(ctx, *, question):  # погуглить
    # сам сайт
    url = 'https://google.gik-team.com/?q=' + str(question).replace(' ', '+')
    # отправка сообщения
    await ctx.send(f'Так как кое кто не умеет гуглить , я сделал это за него.\n{url}')





#https://translate.google.com/?hl=ru





#transletor
@bot.command()
async def translate(ctx, *, question):  # погуглить
    # сам сайт
    url = 'https://translate.google.com/?q=' + str(question).replace(' ', '+')
    # отправка сообщения
    await ctx.send(f'Так как кое кто не умеет переводить , я сделал это за него.\n{url}')










token = os.environ.get("botkey")
client.run(str(token))
