
from flask import Flask

webapp = Flask(__name__)

from app import trivial
from app import product
from app import customer
from app import category

from app import main

