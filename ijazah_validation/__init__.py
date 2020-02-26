from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b578ac34d1c6c2ca4b7f374741ff6c1c'

from ijazah_validation import routes