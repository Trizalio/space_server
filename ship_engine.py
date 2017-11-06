import json
import time
import resourses
import math

from math_wrapper import get_best_mode
from resourses import *
from datetime import date
from math import sqrt

SHIELD_SHIFT = 0.001
SHIELD_BURN = 0.01
SHIELD_SIZE = 10

def add_ship_model(ship_name, width, height):
    ship_json = json.dumps(
        {
            "width":width, 
            "height":height,
            "shield": [0] * int(2 * math.pi * (width + height) / SHIELD_SIZE),

            "a":0, "va":0, 
            "x":0, "vx":0, 
            "y":0, "vy":0, 

            "modules":
            {
                "1":{
                    "cx":15,
                    "cy":0,
                    "width":24,
                    "height":18,
                    "type":"cabin",
                    "isOn":True,
                    "health":50,
                    "mass":15
                },

                "2":{
                    "cx":-15,
                    "cy":0,
                    "width":36,
                    "height":24,
                    "type":"engine",
                    "isOn":True,
                    "engine_angle":math.pi,
                    "engine_power": 50,
                    "power_fraction":0,
                    "health":250,
                    "mass":50
                },

                "3":{
                    "cx":-15,
                    "cy":20,
                    "width":30,
                    "height":16,
                    "type":"engine",
                    "isOn":True,
                    "engine_angle":math.pi,
                    "engine_power": 35,
                    "power_fraction":0,
                    "health":200,
                    "mass":35
                },

                "4":{
                    "cx":-15,
                    "cy":-20,
                    "width":30,
                    "height":16,
                    "type":"engine",
                    "isOn":True,
                    "engine_angle":math.pi,
                    "engine_power": 35,
                    "power_fraction":0,
                    "health":200,
                    "mass":35
                },

                "5":{
                    "cx":7,
                    "cy":20,
                    "width":14,
                    "height":20,
                    "type":"engine",
                    "isOn":True,
                    "engine_angle": math.pi / 2,
                    "engine_power": 20,
                    "power_fraction":0,
                    "health":100,
                    "mass":20
                },

                "6":{
                    "cx":7,
                    "cy":-20,
                    "width":14,
                    "height":20,
                    "type":"engine",
                    "isOn":True,
                    "engine_angle": -math.pi / 2,
                    "engine_power": 20,
                    "power_fraction":0,
                    "health":100,
                    "mass":20
                },
            },

            "a0":0, 
            "img":"space/img/players/" + ship_name + "_base.png"
        }
    )
    ShipModel.create(name=ship_name, json=ship_json)
    print "added", ship_name, width, height


# typhon = ShipModel.create(name='Typhon', 
#     json='{"width":100, "height":50, "shield":[1,2,3,4,5,6,7,8,9,0], "angle":0, "x":0, "y":0, "vx":0, "vy":0}')
# SHIELD_SHIFT = 0.001

def build_ship(ModelName):
    print "build " + ModelName
    Model = ShipModel.get(ShipModel.name == ModelName)
    ty = Ship.create(name='Fo', json=Model.json, manufacture_date=date(1935, 3, 1), model=Model)

def act_all_ships(time_step):
    ships = Ship.select();
    print "act_all", len(ships)
    for i in ships:
        act_ship(i)
        i.save()

def act_ship(ship):
    # print "act_ship", ship
    ship_json = ship.json
    ship_obj = json.loads(ship_json)

    # print ship_obj['shield']
    calculate_engines_effect(ship_obj)

    tasks = ShipModuleTask.select().where(ShipModuleTask.ship == ship)
    target_acc = orders_tick(ship_obj, tasks)

    shield_tick(ship_obj['shield'])
    phisics_tick(ship_obj)
    mass_center_tick(ship_obj)

    modules_tick(ship_obj, ship_obj['modules'])

    # herb_mittens.delete_instance()

    cmap = build_control_map(ship_obj)
    pick_from_control_map2(ship_obj, cmap, target_acc[0], target_acc[1], target_acc[2])

    # print ship_obj['shield']
    ship.json = json.dumps(ship_obj)

def shield_tick(shield):
    # print type(1.5)
    for i, si in enumerate(shield):
        # print type(si)
        index = len(shield) - 1
        if i:
            index = i - 1
        # print 'index', index
        si2 = shield[index]
        # print 'si', si
        # print 'si2', si2
        delta = si2 - si
        # print 'delta', delta
        shift = delta * SHIELD_SHIFT
        # print 'shift', shift
        shield[i] += shift
        shield[index] -= shift
        shield[index] += SHIELD_BURN * 100
        shield[index] *= 1 - SHIELD_BURN
    # print shield
    return shield

def phisics_tick(ship_obj):
    ship_obj["x"] += ship_obj["vx"]
    ship_obj["y"] += ship_obj["vy"]
    ship_obj["a"] += ship_obj["va"]
    # ship_obj["va"] = SHIELD_SHIFT * 10

def mass_center_tick(ship_obj):
    total_mass = 0
    mmx = 0
    mmy = 0
    modules = ship_obj['modules']
    for module in modules.itervalues():
        mass = module['mass']
        mmx += module['cx'] * mass
        mmy += module['cy'] * mass
        total_mass += mass

    mx = mmx / total_mass
    my = mmy / total_mass

    ship_obj["mx"] = 0
    ship_obj["my"] = 0
    if mx or my:
        ship_obj["x"] += mx
        ship_obj["y"] += my
        for module in modules.itervalues():
            module['cx'] -= mx
            module['cy'] -= my

# def shield_size_tick(ship_obj):
#     outer_points = []
#     modules = ship_obj['modules']
#     for module in modules.itervalues():
#         cx = module['cx']
#         if cx > 0:
#             cx += module['width'] / 2
#         else:
#             cx -= module['width'] / 2
#         cy = module['cy']
#         if cy > 0:
#             cy += module['height'] / 2
#         else:
#             cy -= module['height'] / 2
#         outer_points.append((cx, cy))


#     # width = ship_obj["width"]
#     # height = ship_obj["height"]

#     width = 1
#     height = 1

#     for point in outer_points:
        

def get_modules_by_filters(ship_obj, filters):
    result = []
    modules = ship_obj['modules']
    for module in modules.itervalues():
        fine = True
        for fil in filters:
            # print 'filter', fil
            module_attribute_value = module[fil['attribute']]
            # print 'module`s value', fil['attribute'], 'is:', module_attribute_value, 'target:', fil['value']
            if module_attribute_value != fil['value']:
                fine = False
        if fine:
            result.append(module)
    return result


def build_control_map(ship_obj):
    print 'build_control_map'
    engines = get_modules_by_filters(ship_obj, [{'attribute':'type', 'value':'engine'}])
    print len(engines), engines

    control_map = {}
    for i in range(0, 2 ** len(engines)):
        vx = 0
        vy = 0
        va = 0

        for module_counter in range(0, len(engines)):
            module = engines[module_counter]
            if (i >> module_counter) % 2 == 0:
                continue

            engine_angle = module['engine_angle']
            liner_part = module['liner_part']
            radial_part = module['radial_part']
            engine_power = module['engine_power']

            vx -= math.cos(engine_angle) * liner_part * engine_power
            vy -= math.sin(engine_angle) * liner_part * engine_power
            va += radial_part * engine_power

            vx = round(vx, 5)
            vy = round(vy, 5)
            va = round(va, 5)

        control_map[(vx, vx, va)] = i
        print i
    print len(control_map), control_map
    return control_map

def pick_from_control_map2(ship_obj, control_map, vx, vy, va):
    task = (vx, vy, va)

    engines = get_modules_by_filters(ship_obj, [{'attribute':'type', 'value':'engine'}])

    if task in control_map:
        for module_counter in range(0, len(engines)):
            print 'engine #', module_counter
            module = engines[module_counter]
            engines_mode = control_map[task]
            if (engines_mode >> module_counter) % 2:
                module['power_fraction'] = 1
                print 'engine is on'
            else:
                module['power_fraction'] = 0
                print 'engine is off'
        return

    # try:
    picked = get_best_mode(control_map, task)
    # except Exception as e:
    #     print e
        # raise e
        # return
    engine_powers = []

    base_mode = picked['base']

    for module_counter in range(0, len(engines)):
        print 'engine #', module_counter
        # module = engines[module_counter]
        engines_mode = base_mode
        if (engines_mode >> module_counter) % 2:
            engine_powers += [1]
            # module['power_fraction'] = 1
            # print 'engine is on'
        else:
            engine_powers += [0]
            # module['power_fraction'] = 0
            # print 'engine is off'

    print 'base', engine_powers
    engine_modifications = list(engine_powers)

    for mode, fraction in picked['shifts'].iteritems():
        for module_counter in range(0, len(engines)):
            print 'engine #', module_counter
            # module = engines[module_counter]
            # engines_mode = picked['base']
            # delta_mode = base_mode - mode
            if (mode >> module_counter) % 2 and engine_powers[module_counter] == 0:
                engine_modifications[module_counter] += fraction
                # module['power_fraction'] = 1
                # print 'engine is on'
            elif engine_powers[module_counter] == 1:
                engine_modifications[module_counter] -= fraction

    for i in range(0, len(engines)):
        print 'engine #', i
        engine = engines[i]
        engine_powers[i] += engine_modifications[i]
        print engine_powers[i], engine_modifications[i]
        if engine_powers[i] > 1:
            engine_powers[i] = 1
        if engine_powers[i] < 0:
            engine_powers[i] = 0
        engine['power_fraction'] = engine_powers[i]
        print 'result', engine_powers[i]

    return

def pick_from_control_map(ship_obj, control_map, vx, vy, va):
    task = (vx, vy, va)
    print '!!!'
    print control_map
    print '!!!'

    engines = get_modules_by_filters(ship_obj, [{'attribute':'type', 'value':'engine'}])

    if task in control_map:
        for module_counter in range(0, len(engines)):
            print 'engine #', module_counter
            module = engines[module_counter]
            engines_mode = control_map[task]
            if (engines_mode >> module_counter) % 2:
                module['power_fraction'] = 1
                print 'engine is on'
            else:
                module['power_fraction'] = 0
                print 'engine is off'
        return 

    dimensions = 3

    nearest = {}
    print 'nearest', nearest

    for key in control_map:
        print 'control_map', control_map
        print 'key', key
        engines_mode = control_map[key]
        nearest_key = ''
        delta_range = 0
        for i in range(0, dimensions):
            delta = key[i] - task[i]
            print 'delta', i, delta
            delta_range += delta ** 2
            if delta > 0:
                nearest_key += '1'
            else:
                nearest_key += '0'
        # delta_range = sqrt(delta_range)
        print 'delta_range', delta_range

        print 'nearest_key', nearest_key
        if nearest_key not in nearest or nearest[nearest_key]['range'] > delta_range:
            nearest[nearest_key] = {'range':delta_range, 'engines_mode':engines_mode}
            print 'nearest updated'

        print 'nearest', nearest

    result = []

    for module_counter in range(0, len(engines)):
        print 'engine #', module_counter
        module = engines[module_counter]
        enumerator = 0
        denumerator = 0
        for mode_dict in nearest.itervalues():
            engines_mode = mode_dict['engines_mode']
            delta_range = mode_dict['range']
            inversed_range = 1 / (delta_range)
            on = False
            if (engines_mode >> module_counter) % 2:
                enumerator += inversed_range
                on = True
            print 'mode', engines_mode , ', delta_range', delta_range, 'inversed_range', inversed_range, 'engine is', on
            denumerator += inversed_range
            print enumerator , '/', denumerator

        power_fraction = enumerator / denumerator
        print "engine", module_counter, 'set to', power_fraction * 100, "%"

        module['power_fraction'] = power_fraction

        result.append(power_fraction)

    print(result)
    print "-------------------------------------"
        # print key
    # print nearest

    # data[min(data.keys(), key=lambda k: abs(k-num))]

def calculate_engines_effect(ship_obj):
    print 'calculate_engines_effect'
    engines = get_modules_by_filters(ship_obj, [{'attribute':'type', 'value':'engine'}])
    print len(engines), engines

    for module in engines:
        delta_x = module['cx']
        delta_y = module['cy']
        delta_range = math.sqrt(delta_x * delta_x + delta_y * delta_y)
        delta_angle = math.atan2(delta_y, delta_x)
        engine_angle = module['engine_angle']
        angle_diff = delta_angle - engine_angle
        liner_part = math.cos(angle_diff)
        radial_part = math.sin(angle_diff)

        module['liner_part'] = liner_part
        module['radial_part'] = radial_part



def orders_tick(ship_obj, tasks):
    modules = ship_obj['modules']
    # print modules
    # print tasks
    target_acc = (0,0,0)
    for task in tasks:
        print "!!!", task

        module_name = task.module
        task_data = json.loads(task.task)
        order = task_data['task']
        task.delete_instance()

        if order == 'acc':        
            vx = task_data['vx']
            vy = task_data['vy']
            va = task_data['va']
            target_acc = (vx, vy, va)
            continue

        if module_name not in modules:
            print 'critical', module_name, ' not in modules'
            continue
        module = modules[module_name]

        print order
        if order == 'setOn':
            module['isOn'] = True
            print "set On"
        if order == 'setOff':
            module['isOn'] = False
            print "set Off"

        if order == 'detach':
            modules.pop(module_name, None)
            # module['isOn'] = False
            print "detached"


    return target_acc
    pass

def modules_tick(ship_obj, modules):
    mx = ship_obj["mx"]
    my = ship_obj["my"]
    for module in modules.itervalues():
        module_type = module['type']
        module_is_on = module['isOn']
        
        if module_type == 'engine' and module_is_on:
            # delta_x = module['cx']
            # delta_y = module['cy']
            # delta_range = math.sqrt(delta_x * delta_x + delta_y * delta_y)
            # delta_angle = math.atan2(delta_y, delta_x)
            engine_angle = module['engine_angle']
            # angle_diff = delta_angle - engine_angle
            # liner_part = math.cos(angle_diff)
            # radial_part = math.sin(angle_diff)
            liner_part = module['liner_part']
            radial_part = module['radial_part']
            power_fraction = module['power_fraction']


            engine_power = module['engine_power'] * power_fraction * SHIELD_BURN * 1
            ship_angle = ship_obj["a"]
            ship_obj["vx"] -= math.cos(engine_angle + ship_angle) * liner_part * engine_power
            ship_obj["vy"] -= math.sin(engine_angle + ship_angle) * liner_part * engine_power
            ship_obj["va"] += radial_part * engine_power / 50

    pass

def addShipModels():
    add_ship_model("striker", 15, 5)
    add_ship_model("miner", 50, 20)
    add_ship_model("cruiser", 150, 100)
    add_ship_model("mothership", 500, 350)

def build_ship(ModelName):
    print "build " + ModelName
    model = ShipModel.get(ShipModel.name == ModelName)
    ty = Ship.create(name='Fo', json=model.json, manufacture_date=date(1935, 3, 1), model=model)

# build_ship('striker')
print "engine started"
query = ShipModuleTask.delete()
query.execute()
print "old tasks deleted"
query = Ship.delete()
query.execute()
print "old ships deleted"
query = ShipModel.delete()
query.execute()
print "old ship models deleted"
addShipModels()
print "new ship models added"
build_ship("miner")
print "new ship added"

while(True):
    act_all_ships(0)
    time.sleep(1 / 1)