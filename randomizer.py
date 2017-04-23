import datetime
from models import  Assassin, Mission
from random import  shuffle
import csv


def build_database():
    with open ('resources/names.csv') as f:
        csv_file = csv.DictReader(f)
        for row in csv_file:
            assassin = Assassin()
            assassin.name = row['name']
            assassin.email = row['email']
            assassin.save()



def assign_targets():
    alive = Assassin.objects(killed_time=None)

    random_list = range(0, alive.count())
    shuffle(random_list)

    i = 0
    for a in alive:
        a.random_order = random_list[i]
        i += 1
        a.save()

    alive_sorted = Assassin.objects(killed_time=None).order_by('random_order')
    i = 1
    count = alive_sorted.count()
    if count > 0:
        first = alive_sorted[0]

    for a in alive_sorted:
        if i < count > 0:
            target = alive_sorted[i]
        else:
            target = first

        mission = Mission()
        print(type(target))
        mission.target = target
        a.targets.append(mission)

        a.save()

        i += 1






