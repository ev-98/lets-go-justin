import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import matchupdata
import framedata
import config

ints = discord.Intents.all()

client = commands.Bot(command_prefix='3s.',intents=ints)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('3s.help'))
    print('Bot is ready')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pinging @ {round(client.latency * 1000)}ms')

@client.command()
async def help(ctx):
    embed=discord.Embed(title="lets-go-justin", url="https://github.com/ev-98/lets-go-justin", description="A Street Fighter III: 3rd Strike resource bot.")
    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/logopedia/images/b/be/SFIII_Online_Edition_Logo.png/revision/latest/scale-to-width-down/1000?cb=20140206180354")
    embed.add_field(name="##Commands (prefix '3s.')", value="8ball: let the third strike announcer decide your fortune\nframes [character] [move]: display frame data\nfortune: see 8ball\nmu [character1] [character2]: display matchup odds\nplay: play a random track from the OST\nstop: stop playing music", inline=False)
    embed.add_field(name="##Character codes", value="For any commands, you may type out the 2-letter character code instead of the full name if you prefer.\nAkuma/Gouki: AK/GO\nAlex: AL\nChun-Li: CH\nDudley: DU\n...etc", inline=False)
    embed.add_field(name="##Move notation", value="The command notation for a normal move is [button] or [input].[button]\nThe notation for special moves are [motion].[button]\nSuper arts are denoted as sa1, sa2, sa3\nClose moves begin with 'close.'\nAerial moves begin with 'air.'\n\nInputs:\nc(crouch), f(forward), b(back), u(up), df, db, uf, ub, hold\nMotions:\nqcf, qcb, hcf, hcb, 360, dp, rapid, charge\nButtons:\nlp, mp, hp, 2p\nlk, mk, hk, 2k\n\nExamples:\nc.mk(crouching medium), charge.2k(ex spinning bird kick), air.qcf.2p (ex kunai), lp+lk(throw), mp+mk(universal overhead)", inline=True)
    embed.set_footer(text="All sprites and music property of Capcom | Frame data and sprites provided by http://wiki.supercombo.com/")
    await ctx.send(embed=embed)

@client.command(aliases=['8ball', 'fortune'])
async def _8ball(ctx, *, msg):
    responses=['Yeah, that makes sense!', 'Well, I got the picture!', 'Yeah, I see!', 'Yeah, I\'ve been waiting for this!', 'Alright, that\'s cool!', 'That\'s what I expected!', 'You need to practice more.', 'We await your return, warrior..', 'Excellent job!']
    await ctx.send(f'{random.choice(responses)}')

@client.command()
async def mu(ctx, c1, c2):
    arg = get_mu(c1,c2)
    await ctx.send(arg)

@client.command()
async def frames(ctx, c1, mv):
    arg = get_frames(c1,mv)
    if arg[1] != 'error':
        fileurl = arg[1]
        file = discord.File(fileurl, filename="image.gif")
        arg[0].set_image(url = 'attachment://image.gif' )
        await ctx.send(embed=arg[0], file=file)
    else:
        print(arg[0])
        await ctx.send(arg[0])

@client.command()
async def play(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        songbank = ['piano.mp3', 'piano2.mp3']
        currentsong = random.choice(songbank)
        source = FFmpegPCMAudio(currentsong)
        player = voice.play(source)
        await ctx.send(f'Now playing: {currentsong}')
    else:
        await ctx.send("You must join a voice channel before playing music!")

@client.command()
async def stop(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel!")
    else:
        await ctx.send("I'm not in a voice channel!")


def get_mu(c1,c2):
    c1=c1.strip()
    c1=c1.upper()
    c2=c2.strip()
    c2=c2.upper()
    # checking arg1
    if c1=='YU'or c1=='YUN':
        i1=0
    elif c1=='CH'or c1=='CHUN-LI'or c1=='CHUNLI'or c1=='CHUN'or c1=='CHUNNERS'or c1=='CHUNNY' or c1=="CHUN_LI":
        i1=1
    elif c1=='KE'or c1=='KEN':
        i1=2
    elif c1=='MA'or c1=='MAKOTO':
        i1=3
    elif c1=='DU'or c1=='DUDLEY':
        i1=4
    elif c1=='YA'or c1=='YANG':
        i1=5
    elif c1=='GO'or c1=='GOUKI'or c1=='AK'or c1=='AKUMA':
        i1=6
    elif c1=='UR'or c1=='URIEN':
        i1=7
    elif c1=='RY'or c1=='RYU':
        i1=8
    elif c1=='OR'or c1=='ORO':
        i1=9
    elif c1=='IB'or c1=='IBUKI':
        i1=10
    elif c1=='EL'or c1=='ELENA':
        i1=11
    elif c1=='NE'or c1=='NECRO':
        i1=12
    elif c1=='AL'or c1=='ALEX':
        i1=13
    elif c1=='RE'or c1=='REMY':
        i1=14
    elif c1=='Q':
        i1=15
    elif c1=='HU'or c1=='HUGO':
        i1=16
    elif c1=='12'or c1=='TW'or c1=='TWELVE':
        i1=17
    elif c1=='SE'or c1=='SEAN':
        i1=18
    else:
        return f'No character found at `{c1}`. Please check for correct spelling and spacing.'
    
    #checking arg2
    if c2=='YU'or c2=='YUN':
        i2=0
    elif c2=='CH'or c2=='CHUN-LI'or c2=='CHUNLI'or c2=='CHUN'or c2=='CHUNNERS'or c2=='CHUNNY' or c2=="CHUN_LI":
        i2=1
    elif c2=='KE'or c2=='KEN':
        i2=2
    elif c2=='MA'or c2=='MAKOTO':
        i2=3
    elif c2=='DU'or c2=='DUDLEY':
        i2=4
    elif c2=='YA'or c2=='YANG':
        i2=5
    elif c2=='GO'or c2=='GOUKI'or c2=='AK'or c2=='AKUMA':
        i2=6
    elif c2=='UR'or c2=='URIEN':
        i2=7
    elif c2=='RY'or c2=='RYU':
        i2=8
    elif c2=='OR'or c2=='ORO':
        i2=9
    elif c2=='IB'or c2=='IBUKI':
        i2=10
    elif c2=='EL'or c2=='ELENA':
        i2=11
    elif c2=='NE'or c2=='NECRO':
        i2=12
    elif c2=='AL'or c2=='ALEX':
        i2=13
    elif c2=='RE'or c2=='REMY':
        i2=14
    elif c2=='Q':
        i2=15
    elif c2=='HU'or c2=='HUGO':
        i2=16
    elif c2=='12'or c2=='TW'or c2=='TWELVE':
        i2=17
    elif c2=='SE'or c2=='SEAN':
        i2=18
    else:
        return f'No character found at `{c2}`. Please check for correct spelling and spacing.'
   
    return matchupdata.matchups[i1][i2]


def get_frames(c1,mv):
    c1=c1.strip()
    c1=c1.upper()
    mv=mv.lower()

 # checking args
    if c1=='YU'or c1=='YUN':
        data = next((item for item in framedata.yun.yun_frames if item["name"] == mv), None)
    elif c1=='CH'or c1=='CHUN-LI'or c1=='CHUNLI'or c1=='CHUN'or c1=='CHUNNERS'or c1=='CHUNNY' or c1=="CHUN_LI":
        data =next((item for item in framedata.chun.chun_frames if item["name"] == mv), None)
    elif c1=='KE'or c1=='KEN':
        data =next((item for item in framedata.ken.ken_frames if item["name"] == mv), None)
    elif c1=='MA'or c1=='MAKOTO':
        data =next((item for item in framedata.makoto.makoto_frames if item["name"] == mv), None)
    elif c1=='DU'or c1=='DUDLEY':
        data = next((item for item in framedata.dudley.dudley_frames if item["name"] == mv), None)
    elif c1=='YA'or c1=='YANG':
        data = next((item for item in framedata.yang.yang_frames if item["name"] == mv), None)
    elif c1=='GO'or c1=='GOUKI'or c1=='AK'or c1=='AKUMA':
        data = next((item for item in framedata.gouki.gouki_frames if item["name"] == mv), None)
    elif c1=='UR'or c1=='URIEN':
        data = next((item for item in framedata.urien.urien_frames if item["name"] == mv), None)
    elif c1=='RY'or c1=='RYU':
        data =next((item for item in framedata.ryu.ryu_frames if item["name"] == mv), None)
    elif c1=='OR'or c1=='ORO':
        data = next((item for item in framedata.oro.oro_frames if item["name"] == mv), None)
    elif c1=='IB'or c1=='IBUKI':
        data =next((item for item in framedata.ibuki.ibuki_frames if item["name"] == mv), None)
    elif c1=='EL'or c1=='ELENA':
        data =next((item for item in framedata.elena.elena_frames if item["name"] == mv), None)
    elif c1=='NE'or c1=='NECRO':
        data = next((item for item in framedata.necro.necro_frames if item["name"] == mv), None)
    elif c1=='AL'or c1=='ALEX':
        data = next((item for item in framedata.alex.alex_frames if item["name"] == mv), None)
    elif c1=='RE'or c1=='REMY':
        data = next((item for item in framedata.remy.remy_frames if item["name"] == mv), None)
    elif c1=='Q':
        data = next((item for item in framedata.q.q_frames if item["name"] == mv), None)
    elif c1=='HU'or c1=='HUGO':
        data = next((item for item in framedata.hugo.hugo_frames if item["name"] == mv), None)
    elif c1=='12'or c1=='TW'or c1=='TWELVE':
        data = next((item for item in framedata.twelve.twelve_frames if item["name"] == mv), None)
    elif c1=='SE'or c1=='SEAN':
        data = next((item for item in framedata.sean.sean_frames if item["name"] == mv), None)
    else:
        print('No char data')
        return f'No character found at `{c1}`. Please check for correct spelling and spacing.', 'error'

    if data:
        embed=discord.Embed(title=data["name"], description=data["desc"], color=0xffffff)
      
        filename = data["pic"]
        embed.add_field(name="Damage", value=data["damage"], inline=True)
        embed.add_field(name="Startup", value=data["startup"], inline=True)
        embed.add_field(name="Hit", value=data["hit"], inline=True)
        embed.add_field(name="Recovery", value=data["recovery"], inline=True)
        embed.add_field(name="Block advantage", value=data["block_adv"], inline=True)
        embed.add_field(name="Hit advantage", value=data["hit_adv"], inline=True)
        return embed, filename
    else:
        print('No move data')
        return f'No move found at `{mv}`. Please check for correct spelling and spacing.', 'error'
        



client.run(config.token)