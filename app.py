from flask import Flask ,render_template ,request
from model import Models 
app = Flask(__name__)


@app.route("/" , methods=['GET','POST'])
def ModelPredict():
    if request.method == "POST" :
        try:
            day=request.form["day"]
            month=request.form["month"]
            year=request.form["year"]
            open=request.form["open"]
            high=request.form["high"]
            low=request.form["low"]
            volume=request.form["volume"]
            S=Models() 
            sentimental_text= request.form["sentiment"]
            res=S.predict_market(day,month,year,open,high,low,volume,sentimental_text)
            return render_template("index.html" , Sscore=res)
        except:
            return render_template("index.html" )
    else:
        return render_template("index.html" )


if __name__ == "__main__":
    app.run()

