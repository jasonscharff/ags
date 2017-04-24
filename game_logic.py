from datetime import  datetime, timedelta
from models import  Assassin, Mission
from random import  shuffle
import csv
from mailer import send_post_kill, send_new_target






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
        mission.target = target
        a.targets.insert(0, mission)

        a.save()
        send_new_target(email_address=a.email, target_name=target.name,assasssin_name=a.name)

        i += 1


def mark_dead(target_name):
    target = Assassin.objects(name__iexact=target_name).first()
    if target is None:
        return False

    killed_time = datetime.utcnow()


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
    current_count = assassin.interval_kill_count
    assassin.interval_kill_count = current_count + 1
    new_mission = target.targets[0]
    new_mission.time = killed_time
    assassin.targets.insert(0, new_mission)

    target.killed_time = killed_time
    target.save()
    assassin.save()

    send_post_kill(email_address=assassin.email, target_name=new_mission.target.name,assasssin_name=assassin.name)





INITIAL_KILL_PERIOD = 2 #in days
INITIAL_KILL_PERIOD_AVERAGE = 1.5
MIN_KILLS_PER_DAY = 1

GAME_START_TIME = datetime(year=2017,month=4,day=24,hour=12)

CLEARED_THRESHOLD = False

def kill_inactive():
    global CLEARED_THRESHOLD
    if CLEARED_THRESHOLD is False:
        if datetime.utcnow() > GAME_START_TIME + timedelta(days=INITIAL_KILL_PERIOD):
            to_die = Assassin.objects(interval_kill_count__lt=INITIAL_KILL_PERIOD_AVERAGE * INITIAL_KILL_PERIOD, killed_time=None)
            for a in to_die:

                if a.kill_exemption + a.interval_kill_count < INITIAL_KILL_PERIOD_AVERAGE * INITIAL_KILL_PERIOD:
                    a.killed_time = datetime.utcnow()
                    a.save()

            CLEARED_THRESHOLD = True
            reset_kill_interval_count()
    else:
        to_die = Assassin.objects(interval_kill_count__lt=MIN_KILLS_PER_DAY, killed_time=None)
        for a in to_die:
            if a.kill_exemption + a.interval_kill_count < MIN_KILLS_PER_DAY:
                a.killed_time = datetime.utcnow()
                a.save()

        reset_kill_interval_count()



def reset_kill_interval_count():
    alive = Assassin.objects(killed_time=None)
    for a in alive:
        a.interval_kill_count = 0
        a.kill_exemption = 0
        a.save()