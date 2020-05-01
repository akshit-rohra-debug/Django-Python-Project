from django.db import models
from . import input
import pandas as pd
from . import imdb_acc
from . import yelp_acc
from . import amazon_acc
# Create your models here.
def accuracy_amazon():
    return amazon_acc.itsmain()

def predict_amazon(comment):
    return input.createmodel(comment)


def predict_imdb(comment):
    return input.createmodel(comment)

def predict_yelp(comment):
    return input.createmodel(comment)

def accuracy_imdb():
    return imdb_acc.itsmain()

def accuracy_yelp():
    return yelp_acc.itsmain()