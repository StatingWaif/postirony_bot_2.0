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
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))

border = '------------------------'

postValue = '\
**!postpic** - классическая картинка\n \
**!kindpic** - добрая картинка \n \
**!rompic** - романтичная картинка для общения с дамами \n \
**!agrpic** - агрессивная картинка \n \
**!schoolpic** - школьная картинка \n \
**!villpic** - деревенская картинка \n \
**!progpic** - погромистская картинка \n \
'

otherValue = '\
**!gachipic** - гачимучи картинка\n \
**!jojopic** - jojo мем\n \
**!memepic** - english meme\n \
**!papichpic** - несмешная картинка с папичем\n \
**!girlpic** - картинка с полуголой женщиной(**NSFW**)\n \
**!hentaipic** - хентай картинка(**NSFW**)\n \
'

notPicValue = '\
**!help** - список команд \n \
**!hello** - поздороваться с ботом\n \
**!weather** **город** - погода в этом городе\n \
**!what** **слово** - определение этого слова \n \
**!blacklist** - если при вызове картинки пришло не связанное с темой картинки нечто(пустой экран, сообщения с рекламой или донатами),\n \
то вызовите эту команду после прихода картинки\n \
**!picsource** - источники картинок бота \
'

musicValue = '\
**!sr название** - заказать музыку(а можно и плейлист)(youtube ссылка или название)\n \
**!skip** - пропустить музыку\n \
**!cursong** - текущая музыка\n \
**!pause** - пауза\n \
**!resume** - возобновление музыки \n \
**!songlist** - список музыки в очереди \n \
**!clearq** - очистить очередь \n \
'

links1 = '\
[postpic](https://vk.com/memnij)\n\
[kindpic](https://vk.com/kind_post)\n\
[rompic](https://vk.com/devkironiya)\n\
[agrpic](https://vk.com/agrironia)\n\
[schoolpic](https://vk.com/chomemi)\n\
[villpic](https://vk.com/postironiya2006)\n\
[progpic](https://vk.com/postironyaprogrammistov)\n\
'

links2 = '\
[gachipic](https://vk.com/gachimuchi)\n\
[jojopic](https://vk.com/dankjojomemes)\n\
[memepic](https://vk.com/reddit)\n\
[papichpic](https://vk.com/papicheveryday)\n\
[girlpic](https://vk.com/geekgirls)\n\
[hentaipic](https://vk.com/club_1_15)\n\
'

