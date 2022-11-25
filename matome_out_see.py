from urllib import request
from flask import render_template
import requests
from bs4 import BeautifulSoup
import budoux
import re
import os
import shutil

from common import kaigyo







def output_see(load_url,rows,words,file_name,remove_anker,auto_kaigyo):
    # load_url = "http://kidan-m.com/archives/26256231.html"
    response = request.urlopen(load_url)
    content = response.read()
    response.close()
    html = content.decode()
    print(html)

    soup = BeautifulSoup(html, "html.parser")
    print(soup)

    # elems = soup.find_all('p', class_='ind')
    # elems = soup.find_all('div', class_='t_b')
    # elems = soup.find_all('div', class_=['t_h', 't_b'])
    # //レスヘッダー
    res_h = 't_h'
    # //レスボディ
    res_b = 't_b'
    # レスした人
    res_name = ''
    # イッチ判定
    isIcchi = 'specified'
    # かっこ除去
    removeKakko = False
    # 改行閾値
    cr = 4
    tw_h = 'mtpro-header'
    tw_b = 'mtpro-content'
    parser = budoux.load_default_japanese_parser()
    print(load_url)
    print(soup)
    print(file_name)
    elems = soup.find_all('div', class_=[res_h, res_b, tw_h, tw_b])
    p = re.compile(r"<[^>]*?>")
    characters = ['俺','嫁','間男','私']

    count = 0
    # フォルダ削除
    shutil.rmtree('templates/out')
    # フォルダ作成
    os.mkdir('templates/out')
    file_name = 'templates/out/' + file_name
    # HTML全体を表示する
    f = open(file_name, 'w', encoding='UTF-8')
    f.writelines('<table border="1"><tr><th>名前</th><th>レス</th></tr>')
    res_no = ''
    print('みてね')
    print(elems)
    for elem in elems:
        # print(elem)
        # 固定リンクをスルーする
        if elem.find('div', class_=['kotei-link']):
            continue
        # 二重のres_hタグをスルーする
        if elem.find('div', class_=[res_h, res_b]):
            continue
        # アンカーの中身だけをとる(気団対策)
        if elem.find('div', class_=['anchor']):
            print("みたぞ")
            for anchor in elem.find_all('div', class_=['anchor']):
                #アンカーを消す
                if remove_anker: 
                    anchor.extract()
                else:
                    anchor.unwrap()
        if elem.find('span', class_=['anchor']):
            print("みたよ")
            for anchor in elem.find_all('span', class_=['anchor']):
                #アンカーを消す
                if remove_anker: 
                    anchor.extract()
                else:
                    anchor.unwrap()
        # フェミ松：リプライURLを消す
        if elem.find('a', class_=['mtpro-tweet-link']):
            print("みたよ")
            for anchor in elem.find_all('a', class_=['mtpro-tweet-link']):
                #アンカーを消す
                if remove_anker: 
                    anchor.extract()
                else:
                    anchor.unwrap()
                

        count += 1
        print(count)
        # 名前かレスか判定
        if count == 1:
            # 新規行
            # f.writelines('<tr>')
            if isIcchi in str(elem):
                res_name = 'イッチ男'
            else:
                res_no = str(elem)
                res_name = res_no
            # f.writelines('<td>')
            # f.writelines(res_name)
            # f.writelines('</td>')
        # レスの場合
        rowIdx = 0
        rowCnt = 0
        charCnt = 0
        soumojisu = 0
        speakChar = False
        if count == 2:
            if auto_kaigyo:
                res = kaigyo(str(elem), soumojisu,parser,p,words)
            else:
                res = str(elem)
            # レスの改行数
            brIdx = res.split('<br/>')
            # print(brIdx)
            # print(len(brIdx))
            for item in brIdx:
                # print(item)
                rowCnt += 1
                if len(str.strip(item)) == 0:
                    continue
                if item.isspace():
                    continue
                rowIdx += 1
                print(rowIdx)
                # キャラクターを探す
                if speakChar == False:
                    for character in characters:
                        if character + '「' in item:
                            res_name = character
                            rowIdx = 1
                            speakChar = True
                if rowIdx == 1:
                    f.writelines('<tr>')
                    f.writelines('<td>')
                    f.writelines(res_name)
                    f.writelines('</td>')
                    f.writelines('<td>')
                #brタグが４つ以上の時、セルを改める
                # 4行行目かつ次が最終行でない場合
                print(res_name)
                print(item)
                print(speakChar)
                if ((rowIdx % rows == 0 and len(brIdx) != rowCnt + 1) or (speakChar == True and '」' in item)) and auto_kaigyo:
                    rowIdx = 0
                    # print('改行')
                    if speakChar == True :
                        # f.writelines( item)
                        print(item)
                        print('syaberu')
                        kakkotoji = item.find('」')
                        print(kakkotoji)
                        if removeKakko:
                            item = re.sub(r"[「」]", "", item)
                        item = item.replace(res_name,'')
                        f.writelines(item)
                        if kakkotoji != -1:
                            speakChar = False
                            f.writelines('</td>')
                            f.writelines('</tr>')
                        # //人物の発言が終わった後にレス番号にする
                        res_name = res_no
                    else:
                        f.writelines(item)
                        f.writelines('</td>')
                        f.writelines('</tr>')
                    # 次のセルへ
                    # f.writelines('<tr>')
                    # f.writelines('<td>')
                    # f.writelines(res_name)
                    # f.writelines('</td>')
                    # f.writelines('<td>')
                else:
                    if speakChar == True :
                        item = item.replace(res_name,'')
                        if removeKakko:
                            item = re.sub(r"[「」]", "", item)
                        f.writelines(item)
                    else:
                        f.writelines(item)
                    if len(brIdx) != rowCnt + 1:
                        f.writelines('<br/>')
            f.writelines('</td>')
            f.writelines('</tr>')




            # if str(elem).count('<br/>') >= cr:
            #     a = 0

            # f.writelines('<td>')
            # f.writelines(str(elem))
            # f.writelines('</td>')
            # f.writelines('</tr>')
            count = 0

    f.writelines('</table>')
    f.close()
    # render_template("/myfile.html")