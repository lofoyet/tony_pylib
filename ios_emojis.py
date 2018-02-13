#! /usr/bin/python
# -*- encoding: utf-8 -*-

# In[231]:
from __future__ import print_function

import sys
import re
import pickle
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict


# In[8]:
def emojiConvert5(u_plus_literal):
    uni = "\\U000" + u_plus_literal[-5:]
    return uni.decode('unicode_escape')

# In[214]:


def emojiConvert4(u_plus_literal):
    uni = "\\u" + u_plus_literal[-4:]
    return uni.decode('unicode_escape')

# In[215]:


def emojiConvert2(u_plus_literal):
    uni = "\\u00" + u_plus_literal[-2:]
    return uni.decode('unicode_escape')


def main(ios_version):

    html_doc = "https://emojipedia.org/apple/ios-{}/".format(ios_version)

    # In[24]:

    REGEX_HREF = r"(?<=\/apple\/ios\-{0:s}\.{1:s}\/)[^\/]+".format(
        *ios_version.split("."))

    # In[26]:

    BASE_URL = "https://emojipedia.org/"

    # In[49]:

    r = requests.get(html_doc)
    soup = BeautifulSoup(r.text, 'html.parser')
    agent_urls = []
    for child in soup.findAll("a"):
        name = child.attrs["href"]
        try:
            if name:
                emoji_name_re = re.search(REGEX_HREF, name)
                if emoji_name_re:
                    agent_urls.append(emoji_name_re.group())

            elif not child.isspace():  # leaf node, don't print spaces
                pass
        except TypeError:
            pass
        finally:
            pass

    # In[59]:

    agent_urls.remove(u'changed')
    agent_urls.remove(u'new')
    agent_urls.remove(u'removed')
    agent_urls.remove(u'show_all')

    # In[60]:

    # len(agent_urls)

    # In[158]:

    REGEX_EMOJI_U_HREF = r"(?<=\/emoji\/)[^\/]+(?=\/)"
    REGEX_EMOJI_U_PLUS = r"U\+.+"

    # In[117]:

    # from time_count_down import time_count_down as tcd

    # In[190]:

    emoji_Upcodes = []
    counter = 0
    len_urls = len(agent_urls)
    for agent_url in agent_urls:
        counter += 1
        emoji_url = emoji_url = BASE_URL + agent_url + "/"
        r = requests.get(emoji_url)
        pre_len = len(emoji_Upcodes)
        soup = BeautifulSoup(r.text, 'html.parser')
        this_page_u_p = []
        for child in soup.findAll("a"):
            content = child.children.next()
            if isinstance(content, unicode) and content:
                if "U" in content:
                    cc = content
                    emoji_re = re.search(REGEX_EMOJI_U_PLUS, content)
                    if emoji_re:
                        this_page_u_p.append(emoji_re.group())
        emoji_Upcodes.append(this_page_u_p)
        if not emoji_Upcodes[-1]:
            print("not found this page")
            emoji_Upcodes[-1] = (counter, agent_url)

    # In[191]:

    print("found all emoji == " + str(len(agent_urls) == len(emoji_Upcodes)))

    # In[197]:

    # In[204]:

    # pickle.dump(emoji_Upcodes, open("../data/emoji_literal_list.pkl", "wb"))

    # In[205]:

    all_len_list = []
    for E in emoji_Upcodes:
        for i in E:
            all_len_list.append(len(i[2:]))

    # In[222]:

    set(all_len_list)

    # In[225]:

    true_emoji_list = []
    for E in emoji_Upcodes:
        this_true_emoji = u""
        for i in E:
            if len(i[2:]) == 2:
                this_true_emoji += emojiConvert2(i)
            elif len(i[2:]) == 4:
                this_true_emoji += emojiConvert4(i)
            elif len(i[2:]) == 5:
                this_true_emoji += emojiConvert5(i)
            else:
                print("this shouldn't happen")
        true_emoji_list.append(this_true_emoji)

    # In[232]:

    emoji_dict = OrderedDict()
    for index, this_true_emoji in enumerate(true_emoji_list):
        emoji_dict[agent_urls[index]] = this_true_emoji

    # In[234]:

    for key, value in emoji_dict.iteritems():
        print(key, value)

    # In[235]:

    pickle.dump(emoji_dict, open(
        "emoji_dict_ios{:s}.pkl".format(ios_version), "wb"))

    # In[196]:


if __name__ == '__main__':
    main(sys.argv[1])
