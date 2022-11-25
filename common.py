import re
def kaigyo(item, soumojisu,parser,p,words):
    outSentence = ''
    itemSentence = parser.translate_html_string(item)
    itemSentence = itemSentence.replace('、','、<wbr>')
    itemSentence = itemSentence.replace('。','。<wbr>')
    sentences = itemSentence.split('</br>')
    sentences = re.split('<br/>|<br >|</br>', itemSentence)
    for sentence in sentences:
        soumojisu = 0
        # print(sentence)
        # print('スレ由来の改行')
        if sentence.isspace():
            continue
        wSentences = sentence.split('<wbr>')
        for wSentence in wSentences:

            mojisu = len(p.sub("", wSentence))
            if mojisu == 0:
                continue
            # htmlタグを消してカウントする
            soumojisu += mojisu
            if soumojisu > words:
                soumojisu = mojisu
                outSentence += '<br/>'
                # print('改行')  
            outSentence += wSentence
        outSentence += '<br/>'
    # print('一行')   
    # print(outSentence)
    return outSentence
    # f.writelines(item)


def add_sum_td(f, row,tw_link):
    row = row + 1
    f.writelines('<td>')
    f.writelines('=LEN(B'+str(row)+')')
    f.writelines('</td>')
    if tw_link != '':
        f.writelines('<td>')
        f.writelines(tw_link)
        f.writelines('</td>')

    return row