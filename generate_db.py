import csv
from models import Assassin

def build_database():
    with open ('resources/names.csv') as f:
        csv_file = csv.DictReader(f)
        for row in csv_file:
            assassin = Assassin()
            assassin.name = row['name']
            assassin.email = row['email']
            assassin.save()