import os

original = str(os.environ.get('CLEARDB_DATABASE_URL')).replace('mysql://', '').replace('?reconnect=true', '')
database = original.split('/')[-1]
host = original.split('@')[-1].replace('/' + database, '')
user = original.split(':')[0]
passwd = original.split('@')[0].replace(user + ':', '')

SEND_TOKEN = str(os.environ.get('SEND_TOKEN'))
VK_TOKEN = str(os.environ.get('VK_TOKEN'))
NAME_SEND = str(os.environ.get('NAME_SEND'))

DBL_TOKEN = str(os.environ.get('DBL_TOKEN'))
PYOWM_TOKEN = str(os.environ.get('PYOWM_TOKEN'))
BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))

border = '------------------------------------------'

postValue = '\
**!postpic** - классическая картинка\n \
**!kindpic** - добрая картинка \n \
**!rompic** - романтичная картинка для общения с дамами \n \
**!agrpic** - агрессивная картинка \n \
**!schoolpic** - школьная картинка \n \
**!villpic** - деревенская картинка \n \
'

otherValue = '\
**!gachipic** - гачимучи картинка\n \
**!memepic** - english meme\n \
**!papichpic** - несмешная картинка с папичем\n \
**!girlpic** - картинка с полуголой женщиной(**NSFW**) \
'

notPicValue = '\
**!help** - список команд \n \
**!hello** - поздороваться с ботом\n \
**!weather** + **город** = погода в этом городе\n \
**!what** + **слово** = определение этого слова \
'