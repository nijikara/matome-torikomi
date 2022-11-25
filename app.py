from flask import Flask, render_template
import matome_out
import matome_out_see
from flask import request
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('layout.html', title='Scraping App')

# ↓ /scrapingをGETメソッドで受け取った時の処理
@app.route('/scraping', methods=['GET', 'POST'])
def get():
    field = request.args.get("field","")
    rows = request.args.get('rows') 
    words = request.args.get('words') 
    today = datetime.datetime.now()
    auto_kaigyo = request.args.get('auto_kaigyo')
    remove_anker = request.args.get('anker') 
    file_name = 'myfile' + today.strftime('%Y%m%d%H%M%S') + '.html'
    # matome_out.output(field,int(rows),int(words),file_name,remove_anker)
    matome_out_see.output_see(field,int(rows),int(words),file_name,remove_anker,auto_kaigyo)
    if request.method == 'GET': # GETされたとき
        # print(field)
        print('出力')
        f = open('templates/out/' + file_name, 'r', encoding='UTF-8')

        data = f.read()
        print(data)
        f.close()
        print(file_name)
        return render_template('out/' + file_name,data = data)
    elif request.method == 'POST': # POSTされたとき
        return 'POST'


if __name__ == "__main__":
    app.run(debug=True)