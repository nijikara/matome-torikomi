from flask import Flask, render_template
import matome_out
from flask import request

app = Flask(__name__)
load_url = "http://kidan-m.com/archives/26256231.html"

@app.route('/')
def hello():
    return render_template('layout.html', title='Scraping App')

# ↓ /scrapingをGETメソッドで受け取った時の処理
@app.route('/scraping', methods=['GET', 'POST'])
def get():
    field = request.args.get("field","")
    rows = request.args.get('rows') 
    words = request.args.get('words') 
    matome_out.output(field,int(rows),int(words))
    
    if request.method == 'GET': # GETされたとき
        # print(field)
        print('出力')
        f = open('templates/myfile.html', 'r', encoding='UTF-8')

        data = f.read()
        print(data)

        f.close()
        return render_template('myfile.html',article=data)
    elif request.method == 'POST': # POSTされたとき
        return 'POST'


if __name__ == "__main__":
    app.run(debug=True)