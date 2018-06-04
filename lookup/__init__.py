from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "uCDr%z4a/HTbijlby#k2Tzx"
import lookup.views