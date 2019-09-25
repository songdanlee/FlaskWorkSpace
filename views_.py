from flask import Flask
import datetime
app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/days/")
def days():
    now = datetime.datetime.now()
    t = datetime.datetime(now.year, 1, 1, 0, 0, 0)
    day = (now - t).days

    print((now - t).total_seconds()/60/60/24)
    print(now.strftime("%j"))
    return str(day)

@app.route("/days/<int:year>/<int:month>/<int:day>/")
def days2(year,month,day):
    now = datetime.datetime(year=year,month=month,day=day,hour=0,minute=0,second=0)
    t = datetime.datetime(year=year,month=1,day=1,hour=0,minute=0,second=0)
    day = (now - t).days

    return str(day)



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8000,debug=True)