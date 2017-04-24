import datetime
from models import  Assassin, Mission
from random import  shuffle
import csv
from bson import ObjectId


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
        a.targets.insert(0, mission)

        a.save()

        i += 1


def mark_dead(target_name):
    target = Assassin.objects(name__iexact=target_name).first()
    if target is None:
        return False

    killed_time = datetime.datetime.utcnow()


    #this is actually pretty slow. Might be better to maintain an additional property
    #with the current, but with <1000 elements this is not really problematic.


    assassin = Assassin.objects(__raw__={'targets.0.target' : target.id}).first()

    if assassin is None:
        #should never happen
        return

    killed_mission = Mission()
    killed_mission.time = killed_time
    killed_mission.target = target

    assassin.kills.insert(0, killed_mission)
    new_mission = target.targets[0]
    new_mission.time = killed_time
    assassin.targets.insert(0, new_mission)

    target.killed_time = killed_time
    target.save()
    assassin.save()


    #send email




