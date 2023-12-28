# Posts poems from the complete Du Fu, in original order.

import os
import json
import random
from atproto import Client

dump = json.load(open('dufu.json'))
number_of_poems = sum(len(poem["sets"]) for poem in dump)
today_index = random.randint(1, number_of_poems - 1) # The last one isn't a complete poem so ignore it.

title_n = "十一 十二 十三 十四 十五 十六 十七 十八 十九 二十 一 二 三 四 五 六 七 八 九 十".split()
title_nc = [f'之{n}' for n in title_n]
count = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
title_map = dict(zip(count, title_nc))

the_poem = None
the_set = None
index = 0
title_suffix = ""
while True:
    for poem_set in dump:
        for local_index, poem in enumerate(poem_set["sets"]):
            index += 1
            if index == today_index:
                the_poem = poem
                the_set = poem_set
                if len(poem_set["sets"]) > 1:
                    title_suffix = title_map.get(local_index + 1)
                break
        else:
            continue
        break
    if len(" ".join(the_poem)) > 260:
        continue
    else:
        break

post = ""

title = the_set["title"].split('（')[0]
post += f'{title}{title_suffix}\n\n'

for index, line in enumerate(the_poem):
    if line.endswith('。'):
        post += f'{line}\n'
        continue
    if line.endswith('，'):
        if len(line) > 5:
            post += f'{line}\n'
        else:
            post += f'{line}'
        continue
    if index % 2 == 0:
        if len(line) >= 6:
            post += f'{line}，\n'
        else:
            post += f'{line}，'
    else:
        post += f'{line}。\n'

print(post)
client = Client()
client.login('dufu.bsky.social', os.environ['BSKY_PASSWORD'])
client.send_post(text=post.strip())
