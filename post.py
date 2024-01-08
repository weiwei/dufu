# Posts poems from the complete Du Fu, in original order.

import os
import json
import random
from time import sleep
from atproto import Client, models

def gen_sections(the_poem, first_section_length):
    sections = []
    section = []
    for index, line in enumerate(the_poem, 1):
        limit = first_section_length if len(sections) == 0 else 295
        if line.endswith('。'):
            line = f"{line}\n"
        elif line.endswith('，'):
            if len(line) > 5:
                line = f'{line}\n'
            else:
                line = f'{line}'
        elif index % 2 == 1:
            if len(line) >= 6:
                line = f'{line}，\n'
            else:
                line = f'{line}，'
        elif index % 2 == 0:
            line = f'{line}。\n'
        if real_len(section) + len(line) <= limit:
            section.append(line)
            if len(section) % 2 == 1 and real_len(section) >= limit:
                section.pop()
                sections.append(section)
                section = [line]
        else:
            if len(section) % 2 == 1:
                old_line = section.pop()
                sections.append(section)
                section = [old_line, line]
            else:
                sections.append(section)
                section = [line]
    if section:
        sections.append(section)
    return sections

def real_len(section):
    return len("".join(section))

def main():
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

    for poem_set in dump:
        for local_index, poem in enumerate(poem_set["sets"]):
            index += 1
            if index == today_index:
                the_poem = poem
                the_set = poem_set
                if len(poem_set["sets"]) > 1:
                    title_suffix = title_map.get(local_index + 1)
                break
        if the_poem:
            break

    root_post = ""

    title = the_set["title"].split('（')[0]
    root_post += f'{title}{title_suffix}\n\n'

    sections = gen_sections(the_poem, 295 - len(root_post))


    root_post += "".join(sections[0])

    print(root_post)
    client = Client()
    client.login('dufu.bsky.social', os.environ['BSKY_PASSWORD'])
    root_post_ref = models.create_strong_ref(
        client.send_post(text=root_post.strip())
    )
    if len(sections) == 1:
        return

    post_ref = root_post_ref
    for section in sections[1:]:
        # sleep(5)
        post = "".join(section)
        print(post)
        post_ref = models.create_strong_ref(
            client.send_post(
                text=post.strip(),
                reply_to=models.AppBskyFeedPost.ReplyRef(
                    parent=post_ref, root=root_post_ref
                )
            )
        )

if __name__ == '__main__':
    main()
