from flask import Flask, request, render_template

app = Flask(__name__)



#Page Layout
@app.route('/')
def page_layout():
    return render_template("index.html")

if __name__=='__main__':
    app.run()