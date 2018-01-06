import os, re, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests, tqdm
from bs4 import BeautifulSoup
from urllib.parse import *

import pandas as pd
import numpy as np


MAX_WORKERS = 10


def _get_upjong_codemap():
    url = 'http://comp.fnguide.com/SVO2/asp/SVD_UJRank.asp?pGB=1&gicode=A005930&cID=&MenuYn=Y&ReportGB=&NewMenuID=301&stkGb='
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    scripts = [sc.text for sc in soup('script') if 'selUpjongData' in sc.text]
    if not scripts:
        raise ValueError('Cannot retrive UpjongData')
    script = scripts[0]
    rex = re.compile('var\s* selUpjongData\s*=\s*\"(?P<option>.+?)\"')
    options = rex.search(script).group('option')
    opt_soup = BeautifulSoup(options, 'html.parser')
    ret = []
    for option in opt_soup('option'):
        upjong_cd = option['value']
        upjong_nm = option.text.strip()
        ret.append({upjong_cd: upjong_nm})
    return ret


def _get_rank_analytics(upjong_cd, upjong_nm, cmdText='menu_6_1'):
    url = 'http://comp.fnguide.com/SVO2/common/sp_read_json.asp'
    params = {
        'cmdText': cmdText,
        'IN_U_CD': upjong_cd,
        'IN_SORT': 7,
        'IN_REPORT_GB': 'A',
#         '_':'1514717590244',
        'IN_MARKET_GB': ''
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.content, 'html.parser')
    df = pd.DataFrame(r.json())
    df['업종명'] = upjong_nm
    df['업종코드'] = upjong_cd
    return df


def annotate_upjong_info(cmdText='menu_6_1', max_worker=None):
    codemap = _get_upjong_codemap()
    dfs = []
    max_worker = max_worker or MAX_WORKERS
    workers = min(max_worker, len(codemap))
    print('workers:', workers)
    with ThreadPoolExecutor(workers) as executor:
        todo_list = []
        for cdmap in codemap:
            for cd, nm in cdmap.items():
                future = executor.submit(_get_rank_analytics, cd, nm, cmdText)
                todo_list.append(future)
        done_iter = tqdm.tqdm(as_completed(todo_list), total=len(todo_list))
        for future in done_iter:
            df = future.result()
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True)


def get_rank_table(ntry=3, max_worker=None):
    print('trying to retrive ranging..(ntry: {})'.format(ntry))
    if ntry == 0:
        return
    try:
        print('retriving upjoing table...')
        rank_by_upjong = annotate_upjong_info('menu_6_1', max_worker=max_worker)
        print('retriving index table...')
        rank_by_index = annotate_upjong_info('menu_6_2', max_worker=max_worker)
    except:
        print('faild to retriving retrying...')
        return get_rank_table(ntry-1, max_worker=max_worker)
    else:
        print('retrive success!')
        rank_by_upjong.set_index(['업종코드', 'GICODE'], inplace=True)
        rank_by_index.set_index(['업종코드', 'GICODE'], inplace=True)
        rest_columns = sorted(set(rank_by_index.columns) - set(rank_by_upjong.columns))
        rank_by_index = rank_by_index[rest_columns]
        return pd.merge(rank_by_upjong, rank_by_index, left_index=True, right_index=True)


def save(df, to='.', prefix='Ranking Analytics'):
    now = datetime.datetime.now()
    str_now = now.strftime('%Y-%m-%d %H=%M=%S')
    fname = '{} {}.xlsx'.format(prefix, str_now)
    path = os.path.join(to, fname)
    print('saving to {}...'.format(path))
    df.to_excel(path)

