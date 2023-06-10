import pymongo
from pymongo.mongo_client import MongoClient
from flask import Flask, redirect, url_for, request, \
    render_template, make_response, session, abort, flash
from werkzeug.utils import secure_filename
from mongoDB import *
from pytz import utc
import json
# set session time
from datetime import timedelta
from datetime import datetime
import time

# object_id(쿼리에 있는 _id의 자료형 변환)
from bson.objectid import ObjectId

app = Flask(__name__)


# @app.route('/upload')
# def upload():
#     return render_template('upload.html')
#
#
# @app.route('/uploader', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return '정보통신공학과 2018112143 조연준 <br>file uploaded successfully'
# _time = utc.localize(datetime.datetime.utcnow())


@app.route('/')
def index():
    value = {'login': 0, 'admin': 0}
    if session.get("id"):
        temp = find("user", "id", session.get("id"))
        value = temp['data']
        value['login'] = 1
        if value['id'] == 'admin':
            value['admin'] = 1
        print(value)

    market = find("market", "name", "market")
    value['price'] = findPrices()
    value['market_coin'] = market['data']['coin']
    value['market_money'] = value['price'][0]['price']
    print(value['price'])

    return render_template('index.html', result=value)


@app.route('/market')
def market():
    value = {'login': 0, 'admin': 0}
    if session.get("id"):
        temp = find("user", "id", session.get("id"))
        value = temp['data']
        value['login'] = 1
        if value['id'] == 'admin':
            value['admin'] = 1
        print(value)

    market = find("market", "name", "market")
    value['price'] = findPrices()
    value['market_coin'] = market['data']['coin']
    value['market_money'] = value['price'][0]['price']
    print(value['price'])

    return render_template('market.html', result=value)


@app.route('/post')
def post():
    value = {'login': 0, 'admin': 0}
    if session.get("id"):
        temp = find("user", "id", session.get("id"))
        value = temp['data']
        value['login'] = 1
        if value['id'] == 'admin':
            value['admin'] = 1
        print(value)

    market = find("market", "name", "market")
    value['price'] = findPrices()
    value['post'] = findPosts()
    value['market_coin'] = market['data']['coin']
    value['market_money'] = value['price'][0]['price']
    print(value['price'])

    return render_template('post.html', result=value)


@app.route('/login')
def login():
    value = {'login': 0}
    if session.get("id"):
        return redirect(url_for("index"))

    return render_template('login.html', result=value)


@app.route('/register')
def register():
    value = {'login': 0}
    if session.get("id"):
        return redirect(url_for("index"))

    return render_template('register.html', result=value)


@app.route('/bank')
def bank():
    value = {'login': 0, 'admin': 0}
    if session.get("id"):
        temp = find("user", "id", session.get("id"))
        value = temp['data']
        value['login'] = 1
        if value['id'] == 'admin':
            value['admin'] = 1
        print(value)
    else:
        return redirect(url_for("index"))

    market = find("market", "name", "market")
    value['price'] = findPrices()
    value['market_coin'] = market['data']['coin']
    value['market_money'] = value['price'][0]['price']
    print(value['price'])

    return render_template('bank.html', result=value)


@app.route('/price')
def price():
    if session.get("id"):
        temp = find("user", "id", session.get("id"))
        value = temp['data']
        value['login'] = 1
        if value['id'] == 'admin':
            value['admin'] = 1
        print(value)
    else:
        return redirect(url_for("index"))

    market = find("market", "name", "market")
    value['price'] = findPrices()
    value['market_coin'] = market['data']['coin']
    value['market_money'] = value['price'][0]['price']
    print(value['price'])

    return render_template('price.html', result=value)


@app.route('/change', methods=['POST'])
def priceChange():
    if session.get("id") is None or session.get("id") != 'admin':
        return redirect(url_for("index"))

    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()

    print(int(req_data['price']))
    insert("price", {"price": int(req_data['price']), "time": datetime.utcnow()}, 0, 0)
    return redirect(url_for("index"))


@app.route('/postcoin', methods=['POST'])
def postcoin():
    if session.get("id") is None:
        return redirect(url_for("index"))

    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()

    price = findPrice()
    coin = int(req_data['coin'])

    user = find("user", "id", session.get("id"))['data']
    if user['coin'] < coin:
        return redirect(url_for("index"))

    insert("post", {"price": price, "seller": session.get("id"), "coin": coin}, 0, 0)
    update("user", "id", session.get("id"), {"coin": user['coin'] - coin})
    return redirect(url_for("index"))


@app.route('/signin', methods=['POST'])
def signin():
    if session.get("id"):
        return redirect(url_for("index"))

    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)
    result = find("user", "id", req_data['id'])

    if not result['exist']:
        return redirect(url_for("index"))
        return '존재하지 않는 아이디 입니다.'

    user = result['data']
    if user['pw'] != req_data['pw']:
        return redirect(url_for("index"))
        return '암호가 틀렸습니다.'

    session['id'] = req_data['id']
    session.permanent = True
    return redirect(url_for("index"))
    return '로그인 성공'


@app.route('/signout')
def signout():
    if session.get("id") is None:
        return redirect(url_for("index"))

    session.pop('id')
    return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup():
    if session.get("id"):
        return redirect(url_for("index"))

    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)
    result = insert("user", req_data, "id", req_data['id'])

    print(result)

    return redirect(url_for("index"))
    if result['exist']:
        return '이미 존재하는 아이디 입니다.'
    else:
        return '계정 생성 성공'


@app.route('/sell', methods=['POST'])
def sellCoin():
    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)

    coin = int(req_data['coin'])
    if session.get("id") is None:
        return redirect(url_for("index"))

    user = find("user", "id", session.get("id"))['data']
    market = find("market", "name", "market")['data']
    price = findPrice()
    print("price", price)

    if market['money'] >= coin * price:
        tmp = {"money": user['money'] + coin * price, "coin": user['coin'] - coin}
        update("user", "id", user['id'], tmp)

        tmp = {"money": market['money'] - coin * price, "coin": market['coin'] + coin}
        update("market", "name", "market", tmp)
    return redirect(url_for("index"))


@app.route('/buy', methods=['POST'])
def buyCoin():
    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)

    coin = int(req_data['coin'])
    if session.get("id") is None:
        return redirect(url_for("index"))

    user = find("user", "id", session.get("id"))['data']
    market = find("market", "name", "market")['data']
    price = findPrice()
    print("price", price)

    if user['money'] >= coin * price:
        tmp = {"money": user['money'] - coin * price, "coin": user['coin'] + coin}
        update("user", "id", user['id'], tmp)

        tmp = {"money": market['money'] + coin * price, "coin": market['coin'] - coin}
        update("market", "name", "market", tmp)
    return redirect(url_for("index"))


@app.route('/purchase/<seller>/<price>/<coin>')
def purchaseCoin(seller, price, coin):
    price = int(price)
    coin = int(coin)
    print("pp", seller, price, coin)
    if session.get("id") is None or session.get("id") == seller:
        return redirect(url_for("index"))

    user = find("user", "id", session.get("id"))['data']
    post = findPost(seller, price, coin)

    if user['money'] >= price * coin:
        tmp = {"money": user['money'] - coin * price, "coin": user['coin'] + coin}
        update("user", "id", user['id'], tmp)

        tmp = {"money": market['money'] + coin * price, "coin": market['coin'] - coin}
        update("user", "id", seller, tmp)
    return redirect(url_for("index"))


@app.route('/withdraw', methods=['POST'])
def withdrawMoney():
    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)

    money = int(req_data['money'])
    if session.get("id") is None:
        return redirect(url_for("index"))

    user = find("user", "id", session.get("id"))['data']
    if money <= user['money']:
        tmp = {"money": user['money'] - money}
        update("user", "id", user['id'], tmp)

    return redirect(url_for("index"))


@app.route('/deposit', methods=['POST'])
def depositMoney():
    if dict(request.form):
        req_data = dict(request.form)
    else:
        req_data = request.get_json()
    print(req_data)

    money = int(req_data['money'])
    if session.get("id") is None:
        return redirect(url_for("index"))

    user = find("user", "id", session.get("id"))['data']
    tmp = {"money": user['money'] + money}
    update("user", "id", user['id'], tmp)

    return redirect(url_for("index"))


if __name__ == '__main__':
    # # flash(경고 문구)를 사용하기 위해서 설정
    app.config["SECRET_KEY"] = "Software_Engineering_Coin_Market"

    # session의 지속시간을 설정
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    app.run(host="0.0.0.0", port=8000, debug=True)
