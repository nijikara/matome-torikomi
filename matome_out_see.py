from urllib import request
from flask import render_template
from bs4 import BeautifulSoup
import budoux
import re
import os
import shutil
from common import add_sum_td, kaigyo

def output_see(load_url,rows,words,file_name,remove_anker,auto_kaigyo):
    # load_url = "http://kidan-m.com/archives/57240754.html#more"
    response = request.urlopen(load_url)
    content = response.read()
    response.close()
    html = content.decode()
    print(html)

    soup = BeautifulSoup(html, "html.parser")
    print(soup)

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
    all_row = 1
    # Twitterリンク
    tw_link = ''
    for elem in elems:
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
            for anchor in elem.find_all('a', class_=['mtpro-tweet-link']):
                #リプライURLを消す
                anchor.extract()
        if elem.find('a', class_=['tweet-url username']):
            for anchor in elem.find_all('a', class_=['tweet-url username']):
                #リプライURLを消す
                anchor.extract()
        # フェミ松：twリンク取得
        if elem.find('a', class_=['mtpro-timestamp']):
            for link in elem.find_all('a', class_=['mtpro-timestamp']):
                tw_link = link.get('href')
                

        count += 1
        print(count)
        # 名前かレスか判定
        if count == 1:
            # 新規行
            if isIcchi in str(elem):
                res_name = 'イッチ男'
            else:
                res_no = str(elem)
                res_name = res_no
        # セル内改行判定
        rowIdx = 0
        rowCnt = 0
        soumojisu = 0
        speakChar = False
        if count == 2:
            if auto_kaigyo:
                res = kaigyo(str(elem), soumojisu,parser,p,words)
            else:
                res = str(elem)
            # レスの改行数
            brIdx = res.split('<br/>')
            for item in brIdx:
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
                print('↓アイテム表示')
                print(item)
                print('↑アイテム表示')
                print(speakChar)
                if ((rowIdx % rows == 0 and len(brIdx) != rowCnt + 1) or (speakChar == True and '」' in item)) and auto_kaigyo:
                    rowIdx = 0
                    # print('改行')
                    if speakChar == True :
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
                            all_row = add_sum_td(f,all_row,tw_link)
                            f.writelines('</tr>')
                        # //人物の発言が終わった後にレス番号にする
                        res_name = res_no
                    else:
                        f.writelines(item)
                        f.writelines('</td>')
                        all_row = add_sum_td(f,all_row,tw_link)
                        f.writelines('</tr>')
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
            all_row = add_sum_td(f,all_row,tw_link)
            f.writelines('</tr>')
            count = 0

    f.writelines('</table>')
    f.close()