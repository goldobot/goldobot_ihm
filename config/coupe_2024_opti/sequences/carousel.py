import asyncio
from enum import Enum

from .cheminees import *

ejecteur_gauche_avant = 830
ejecteur_gauche_arriere = 560
ejecteur_gauche_idle = 736

ejecteur_droit_avant = 200
ejecteur_droit_arriere = 460
ejecteur_droit_idle = 285

ejecteur_centre_idle = 495
ejecteur_centre_max = 390

carousel_centre = 14380
carousel_max = 28280
carousel_min = 450
ecart_g_d = 1635

pos_2 = 1280
diff_between_slots = 819.6
turn = 8192
nb_pos = 34


class Slot(Enum):
    EMPTY = 0
    UNKNOWN = 1
    WHITE = 2
    PURPLE = 3

class CarouselStuckException(Exception):
    pass

class EjectorStuckException(Exception):
    pass


class Carousel:
    slots = [Slot.EMPTY for _ in range(10)]

    def __init__(self):
        self.slots = [Slot.EMPTY for _ in range(10)]

    def reset(self):
        self.slots = [Slot.EMPTY for _ in range(10)]

async def carousel_move(pose, torque = 1.0, speed = 1.0, pos_threshold = 40, overload_threshold = 40):
    old_pos = 0
    overload_count = 0

    # Enable Dynamixel
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    # TODO : check ejecteurs position safe

    # Move Dynamixel
    await servos.moveMultiple({'carousel': pose}, speed)

    # Check stuck carrousel
    # If load is over 95% of max and dynamixel is not moving, then we have an issue
    while (servos.states['carousel'].measured_position < pose-pos_threshold) or (servos.states['carousel'].measured_position > pose+pos_threshold):
        old_pos = servos.states['carousel'].measured_position
        if(abs(servos.states['carousel'].measured_load) > (0.95 * torque * 1024)) and (abs(old_pos - servos.states['carousel'].measured_position) < 3):
            overload_count = overload_count + 1
            if overload_count >= overload_threshold:
                await servos.setMaxTorque(['carousel'], 0)
                await servos.setEnable(['carousel'], False)
                await servos.moveMultiple({'carousel': servos.states['carousel'].measured_position}, speed=1.0)
                raise CarouselStuckException()
        else:
            overload_count = 0
        await asyncio.sleep(0.02)

@robot.sequence
async def test_carousel_move():
    await carousel_move(carousel_centre)

@robot.sequence
async def carousel_demo_sponsors():
    # await turbine_d_enable()
    # await turbine_g_enable()
    # await asyncio.sleep(2)
    for i in range(10):
        await slot_cheminee_gauche(i)
        await asyncio.sleep(1)

@robot.sequence
async def test_carousel_move_2():
    await slot_cheminee_droite(3)

@robot.sequence
async def debloque_cheminees():
    _goal = servos.states['carousel'].measured_position
    _goal = _goal + diff_between_slots / 3
    try:
        await carousel_move(_goal)
    except:
        await carousel_move(_goal + diff_between_slots)
    await asyncio.sleep(0.5)
    await porte_d_ferme()
    await porte_g_ferme()
    await asyncio.sleep(0.5)
    await porte_d_ouvre()
    await porte_g_ouvre()

@robot.sequence
async def init_carousel():
    await servos.setMaxTorque(['carousel'], 0.30)
    await servos.setMaxTorque(['ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], 0.50)
    await servos.setEnable(['carousel', 'ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], True)
    await servos.moveMultiple({'ejecteur_gauche': ejecteur_gauche_idle,
                            'ejecteur_centre': ejecteur_centre_idle,
                            'ejecteur_droit': ejecteur_droit_idle}, speed=1.0)
    await asyncio.sleep(0.5)
    await servos.moveMultiple({'carousel': carousel_centre}, speed = 0.5)

@robot.sequence
async def empty_carousel():
    # Activation dynamixels
    torque = 0.3

    await servos.setMaxTorque(['carousel'], torque)
    await servos.setMaxTorque(['ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], 0.40)
    await servos.setEnable(['carousel','ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], True)
    
    await init_turbines()
    await asyncio.sleep(4)
    await turbine_g_suck()
    await turbine_d_suck()
    await slot_ejecteur_gauche(3)
    await asyncio.wait({eject_left(), eject_center(), eject_right()})
    await asyncio.sleep(0.5)
    await slot_ejecteur_gauche(6)
    await asyncio.wait({eject_left(), eject_center(), eject_right()})
    await asyncio.sleep(0.5)
    await slot_ejecteur_gauche(9)
    await asyncio.wait({eject_left(), eject_center(), eject_right()})
    await asyncio.sleep(0.5)
    await slot_ejecteur_gauche(10)
    await eject_left()
    await asyncio.sleep(0.5)
    await init_turbines()

@robot.sequence
async def eject_safe():
    await servos.setMaxTorque(['ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], 0.40)
    await servos.setEnable(['carousel','ejecteur_gauche', 'ejecteur_centre', 'ejecteur_droit'], True)
    await servos.moveMultiple({'ejecteur_gauche': ejecteur_gauche_idle,
                            'ejecteur_centre': ejecteur_centre_idle,
                            'ejecteur_droit': ejecteur_droit_idle}, speed=1.0)

@robot.sequence
async def eject_left():
    overload_threshold = 10
    overload_count = 0
    position_threshold = 5
    torque = 0.6
    await servos.setMaxTorque(['ejecteur_gauche'], torque)
    await servos.setEnable(['ejecteur_gauche'], True)
    await servos.moveMultiple({'ejecteur_gauche': ejecteur_gauche_arriere}, speed=1)
    while (servos.states['ejecteur_gauche'].measured_position < ejecteur_gauche_arriere-position_threshold) or (servos.states['ejecteur_gauche'].measured_position > ejecteur_gauche_arriere+position_threshold):
        if(abs(servos.states['ejecteur_gauche'].measured_load) > (0.95 * torque * 1024)):
            overload_count = overload_count + 1
            if overload_count >= overload_threshold:
                raise Exception("Overload ejecteur gauche")
        await asyncio.sleep(0.01)
    await servos.moveMultiple({'ejecteur_gauche': ejecteur_gauche_idle}, speed=1.0)
        

@robot.sequence
async def eject_center():
    overload_threshold = 10
    overload_count = 0
    position_threshold = 10
    torque = 0.6
    await servos.setMaxTorque(['ejecteur_centre'], torque)
    await servos.setEnable(['ejecteur_centre'], True)
    await servos.moveMultiple({'ejecteur_centre' : ejecteur_centre_max}, speed=1)
    while (servos.states['ejecteur_centre'].measured_position < ejecteur_centre_max-position_threshold) or (servos.states['ejecteur_centre'].measured_position > ejecteur_centre_max+position_threshold):
        if(abs(servos.states['ejecteur_centre'].measured_load) >  (0.95 * torque * 1024)):
            overload_count = overload_count + 1
            if overload_count >= overload_threshold:
                raise Exception("Overload ejecteur centre")
        await asyncio.sleep(0.01)
    await servos.moveMultiple({'ejecteur_centre': ejecteur_centre_idle}, speed=1.0)

@robot.sequence
async def eject_right():
    overload_threshold = 10
    overload_count = 0
    position_threshold = 5
    torque = 0.6
    await servos.setMaxTorque(['ejecteur_droit'], torque)
    await servos.setEnable(['ejecteur_droit'], True)
    await servos.moveMultiple({'ejecteur_droit' : ejecteur_droit_arriere}, speed=1)
    while (servos.states['ejecteur_droit'].measured_position < ejecteur_droit_arriere-position_threshold) or (servos.states['ejecteur_droit'].measured_position > ejecteur_droit_arriere+position_threshold):
        if(abs(servos.states['ejecteur_droit'].measured_load) > (0.95 * torque * 1024)):
            overload_count = overload_count + 1
            if overload_count >= overload_threshold:
                raise Exception("Overload ejecteur droit")
        await asyncio.sleep(0.01)
    await servos.moveMultiple({'ejecteur_droit': ejecteur_droit_idle}, speed=1.0)

@robot.sequence
async def test_slot():
    try:
        await slot_cheminee_gauche(1)
    except:
        pass

async def slot_cheminee_droite(slot):
    position_threshold = 10
    torque = 0.5
    overload_threshold = 10
    overload_count = 0
    old_pos = 0
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    """
    await servos.moveMultiple({'carousel': _goal}, speed=1.0)
    while (servos.states['carousel'].measured_position < _goal-position_threshold) or (servos.states['carousel'].measured_position > _goal+position_threshold):
        old_pos = servos.states['carousel'].measured_position
        if(abs(servos.states['carousel'].measured_load) > (0.95 * torque * 1024)) and (abs(old_pos - servos.states['carousel'].measured_position < 3)):
            overload_count = overload_count + 1
            if overload_count >= overload_threshold:
                await servos.setMaxTorque(['carousel'], 0)
                await servos.setEnable(['carousel'], False)
                await servos.moveMultiple({'carousel': servos.states['carousel'].measured_position}, speed=1.0)
                raise Exception("Overload carrousel")
        await asyncio.sleep(0.01)
    """
    await carousel_move(_goal)

async def slot_cheminee_gauche(slot):
    position_threshold = 10
    torque = 0.5
    overload_threshold = 10
    overload_count = 0
    old_pos = 0
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre + 1639 + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    await carousel_move(_goal)

async def slot_ejecteur_gauche(slot):
    position_threshold = 30
    torque = 0.5
    overload_threshold = 10
    overload_count = 0
    old_pos = 0
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre + 4096 + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    await carousel_move(_goal)

async def slot_ejecteur_centre(slot):
    position_threshold = 10
    torque = 0.5
    overload_threshold = 10
    overload_count = 0
    old_pos = 0
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre + 4915.5 + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    await carousel_move(_goal)

async def slot_ejecteur_droit(slot):
    position_threshold = 10
    torque = 0.5
    overload_threshold = 10
    overload_count = 0
    old_pos = 0
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre + 5735 + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    await carousel_move(_goal)

async def slot_lecteur_rfid(slot):
    position_threshold = 10
    torque = 0.3
    overload_threshold = 10
    overload_count = 0
    old_pos = 0    
    if slot <= 0 or slot > 10:
        return -1
    await servos.setMaxTorque(['carousel'], torque)
    await servos.setEnable(['carousel'], True)

    _pos = round(carousel_centre - 1324 + (slot - 1) * diff_between_slots)
    if _pos > carousel_max:
        _pos = _pos - turn
    elif _pos < carousel_min:
        _pos = _pos + turn
    _current_pos = servos.states['carousel'].measured_position
    _goal = _pos + round((_current_pos - _pos)/8182) * turn

    while _goal > carousel_max:
        _goal = _goal - turn
    while _goal < carousel_min:
        _goal = _goal + turn

    await carousel_move(_goal)

@robot.sequence
async def test_mehdi():
    print("CG : " + str(await get_slot_cheminee_gauche()))
    print("CD : " + str(await get_slot_cheminee_droite()))
    print("EG : " + str(await get_slot_ejecteur_gauche()))
    print("EC : " + str(await get_slot_ejecteur_centre()))
    print("ED : " + str(await get_slot_ejecteur_droit()))

async def get_slot_cheminee_droite():
    _pos = servos.states['carousel'].measured_position
    if _pos < carousel_centre:
        _pos = _pos + 2 * turn
    _diff = abs(_pos - carousel_centre) % turn
    _div = _diff / diff_between_slots
    _rounded_div = round(_div)
    if(abs(_div - _rounded_div) > 0.1):
        return -1
    else:
        return (_rounded_div + 1) % 10
    
async def get_slot_cheminee_gauche():
    _val = await get_slot_cheminee_droite()
    if _val == -1:
        return -1
    else:
        return (_val - 2) % 10

async def get_slot_ejecteur_gauche():
    _val = await get_slot_cheminee_droite()
    if _val == -1:
        return -1
    else:
        return (_val - 5) % 10

async def get_slot_ejecteur_centre():
    _val = await get_slot_cheminee_droite()
    if _val == -1:
        return -1
    else:
        return (_val - 6) % 10

async def get_slot_ejecteur_droit():
    _val = await get_slot_cheminee_droite()
    if _val == -1:
        return -1
    else:
        return (_val - 7) % 10

@robot.sequence
async def center_slot1():
    await eject_safe()
    await slot_ejecteur_centre(1)

@robot.sequence
async def center_slot2():
    await eject_safe()
    await slot_ejecteur_centre(2)

@robot.sequence
async def center_slot3():
    await eject_safe()
    await slot_ejecteur_centre(3)

@robot.sequence
async def center_slot4():
    await eject_safe()
    await slot_ejecteur_centre(4)

@robot.sequence
async def center_slot5():
    await eject_safe()
    await slot_ejecteur_centre(5)

@robot.sequence
async def center_slot6():
    await eject_safe()
    await slot_ejecteur_centre(6)

@robot.sequence
async def center_slot7():
    await eject_safe()
    await slot_ejecteur_centre(7)

@robot.sequence
async def center_slot8():
    await eject_safe()
    await slot_ejecteur_centre(8)

@robot.sequence
async def center_slot9():
    await eject_safe()
    await slot_ejecteur_centre(9)

@robot.sequence
async def center_slot10():
    await eject_safe()
    await slot_ejecteur_centre(10)