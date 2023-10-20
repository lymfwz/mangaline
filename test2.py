import urllib.request

from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import ast

#
# watcher = LolWatcher("RGAPI-7e34a3ac-907f-4f0c-8071-bbb0e35d58e0", default_status_v5=True)
# region = 'kr'

def simpleS(watcher, region):
    #
    latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
    print(latest)

    static_champ_list = watcher.data_dragon.champions(latest, False, 'zh_CN')
    # print(static_champ_list)
    champ_trans = {}  # 英雄列表
    for key in static_champ_list['data']:
        row = static_champ_list['data'][key]
        champ_trans[row['id']] = row['name']

    spells_list = watcher.data_dragon.summoner_spells(latest, 'zh_CN')
    spells_dict = {}  # 召唤师技能列表
    for key in spells_list['data']:
        row = spells_list['data'][key]
        spells_dict[row['key']] = row['name']

    spellno_list = list(spells_dict.keys())  # 召唤师技能编号
    # print(spellno_list)

    item_list = watcher.data_dragon.items(latest, 'zh_CN')
    item_dict = {}
    for key in item_list['data']:
        row = item_list['data'][key]
        item_dict[key] = row['name']

    itemno_list = list(item_dict.keys())  # 装备编号
    # print(itemno_list)

def selectById(watcher, region, player):
    current = watcher.summoner.by_name(region, player)
    print(current)

if __name__ == '__main__':
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }
    my_api = 'RGAPI-7e34a3ac-907f-4f0c-8071-bbb0e35d58e0'
    lol_watcher = LolWatcher(my_api)
    # faker的信息
    region = 'kr'  # Riot API开发文档里有写到各个服务器的region缩写
    summoner_name = 'Hide on bush'
    url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/Hide%20on%20bush'
    request = urllib.request.Request(url, headers=head)



    # 创建一个lol_watcher下的summoner_faker对象
    summoner_faker = urllib.request.urlopen(request)
    print(summoner_faker)