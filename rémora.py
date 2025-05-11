import math
import time
from tkinter import Tk, StringVar, Label, Button, Entry
import krpc

# PID (Code par cybershadow, basé sur un concept d'artwhaley)

#


class PID(object):
    '''
    Generic PID Controller Class
    An instance is created with the format
    your_pid=PID(P=.0001, I=0.00001, D=0.000001)
    Use your_pid.setpoint(X) to set the target output value of the controller.     
    Regularly call your_pid.update(Y), passing it the input data that the
    controller should respond to.
    output_data = your_pid.update(input_data)
    '''

    def __init__(self, P=1.0, I=0.1, D=0.01):
        self.Kp = P  # P Proportion
        self.Ki = I  # I Intégrale
        self.Kd = D  # D Dérivée
        self.P = 0.0
        self.I = 0.0
        self.D = 0.0
        self.SetPoint = 0.0  # Valeur cible
        self.ClampI = 1.0  # Clamp anti-surcorrection
        self.LastTime = time.time()
        self.LastMeasure = 0.0

    def update(self, measure):
        now = time.time()
        change_in_time = now - self.LastTime
        if not change_in_time:
            # workaround si DeltaT > 0
            change_in_time = 1.0

        error = self.SetPoint - measure
        self.P = error
        self.I += error
        self.I = self.clamp_i(self.I)   # Clamp anti-surcorrection
        self.D = (measure - self.LastMeasure) / (change_in_time)

        self.LastMeasure = measure  # T => T-1
        self.lastTime = now

        return (self.Kp * self.P) + (self.Ki * self.I) - (self.Kd * self.D)

    def clamp_i(self, i):
        if i > self.ClampI:
            return self.ClampI
        elif i < -self.ClampI:
            return -self.ClampI
        else:
            return i

    def setpoint(self, value):
        self.SetPoint = value
        self.I = 0.0


p = PID(P=.25, I=0.025, D=0.0025)
p.ClampI = 20
p.setpoint(8000)

# Démarage du serveur et du pilote auto
instance = krpc.connect(name='Rémora Gravity-turn')
vessel = instance.space_center.active_vessel
telem = vessel.flight(vessel.orbit.body.reference_frame)

# Fin Démarage du serveur et du pilote auto

window = Tk()

temps = 0
notlaunched = True
Armed = False

variable_G = StringVar()
variable_Ga = StringVar()
variable_Q = StringVar()
variable_ISP = StringVar()
variable_TV = StringVar()
variable_AT = StringVar()
variable_T = StringVar()
variable_TP = StringVar()
variable_temps = StringVar()
variable_ATP = StringVar()
variable_ADF = StringVar()
variable_AA = StringVar()
variable_VA = StringVar()
variable_AC = StringVar()
variable_Heading = StringVar()
variable_Pitch = StringVar()
variable_Roll = StringVar()

flight_info = vessel.flight()
orbit_info = vessel.orbit

stream_prograde = instance.add_stream(getattr, flight_info, 'prograde')
atmosphere_density = instance.add_stream(
    getattr, flight_info, 'atmosphere_density')
mean_altitude = instance.add_stream(getattr, flight_info, 'mean_altitude')
g_force = instance.add_stream(getattr, flight_info, 'g_force')
dynamic_pressure = instance.add_stream(
    getattr, flight_info, 'dynamic_pressure')
terminal_velocity = instance.add_stream(
    getattr, flight_info, 'terminal_velocity')
apoapsis_altitude = instance.add_stream(
    getattr, orbit_info, 'apoapsis_altitude')
specific_impulse = instance.add_stream(getattr, vessel, 'specific_impulse')
available_thrust = instance.add_stream(getattr, vessel, 'available_thrust')
thrust = instance.add_stream(getattr, vessel, 'thrust')
specific_impulse = instance.add_stream(getattr, vessel, 'specific_impulse')
vessel_direction = instance.add_stream(
    vessel.direction, vessel.surface_reference_frame)
throttle = instance.add_stream(getattr, vessel.control, 'throttle')

stream_prograde.start()
atmosphere_density.start()
mean_altitude.start()
g_force.start()
dynamic_pressure.start()
terminal_velocity.start()
apoapsis_altitude.start()
specific_impulse.start()
available_thrust.start()
thrust.start()
specific_impulse.start()
vessel_direction.start()
throttle.start()


window.title("Système de guidage Rémora")
# window.geometry('700x400')


class labelplusvalue():

    def __init__(self, ligne=0, label="default", variable=0, unit=""):

        self.ligne = ligne
        self.label = label
        self.variable = variable
        self.unit = unit
        self.lbl_label = Label(window, text=label)
        self.lbl_label.grid(column=0, row=ligne)
        self.lbl_label = Label(window, textvariable=variable)
        self.lbl_label.grid(column=1, row=ligne)
        if (self.unit != ""):
            self.lbl_label = Label(window, text=unit)
            self.lbl_label.grid(column=2, row=ligne)


def cross(u, v):
    return (
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0])


def dot(u, v):
    return u[0]*v[0]+u[1]*v[1]+u[2]*v[2]


def magnitude(v):
    return math.sqrt(dot(v, v))


def angle_between_vectors(u, v):
    """ Compute the angle between vector u and v """
    dp = dot(u, v)
    if dp == 0:
        return 0
    um = magnitude(u)
    vm = magnitude(v)
    return math.acos(dp / (um*vm)) * (180. / math.pi)


def getposition(vessel_direction):
    horizon_direction = (0, vessel_direction[1], vessel_direction[2])
    pitch = angle_between_vectors(vessel_direction, horizon_direction)
    if vessel_direction[0] < 0:
        pitch = -pitch
    north = (0, 1, 0)
    heading = angle_between_vectors(north, horizon_direction)
    if horizon_direction[2] < 0:
        heading = 360 - heading
    up = (1, 0, 0)
    plane_normal = cross(vessel_direction, up)
    vessel_up = instance.space_center.transform_direction(
        (0, 0, -1), vessel.reference_frame, vessel_direction())
    roll = angle_between_vectors(vessel_up, plane_normal)
    if vessel_up[0] > 0:
        roll *= -1
    elif roll < 0:
        roll += 180
    else:
        roll -= 180
    print('pitch = % 5.1f, heading = % 5.1f, roll = % 5.1f' %
          (pitch, heading, roll))
    return [heading, pitch, roll]


lblG = labelplusvalue(0, "G", variable_G, "g")
lblGa = labelplusvalue(1, "G", variable_Ga, "m/s²")
lblQ = labelplusvalue(2, "Q", variable_Q, "Pascals")
lblTV = labelplusvalue(3, "Vitesse terminale", variable_TV, "m/s")
lblISP = labelplusvalue(4, "ISP", variable_ISP, "s")
lblAT = labelplusvalue(5, "Poussée disponible", variable_AT, "kN")
lblT = labelplusvalue(6, "Poussée actuelle", variable_T, "kN")
lblTp = labelplusvalue(7, "Poussée actuelle (%)", variable_TP, "%")
lblsp = labelplusvalue(8, "", "", "")
lbltime = labelplusvalue(9, "Temps de vol", variable_temps, "s")
lblATP = labelplusvalue(10, "Angle de la prograde", variable_ATP, "°")
lblADF = labelplusvalue(11, "Densite d'atmoshpère", variable_ADF, "")
lblAA = labelplusvalue(12, "Altitude de l'apoapside", variable_AA, "m")
lblAA = labelplusvalue(13, "Altitude du vaisseau", variable_VA, "m")
lblAC = labelplusvalue(14, "Altitude de calcul", variable_AC, "m")
lblH = labelplusvalue(15, "Cap", variable_Heading, "°")
lblP = labelplusvalue(16, "Assiète", variable_Pitch, "°")
lblR = labelplusvalue(17, "Roulis", variable_Roll, "°")


def launch():
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    global notlaunched, Armed
    notlaunched = False
    Armed = True


btn = Button(window, text="Launch !", command=launch)
btn.grid(column=0, row=19)


def reset():
    global notlaunched, temps, Armed
    notlaunched = True
    temps = 0
    Armed = False


update_timer = 0
btn = Button(window, text="Reset Timer", command=reset)
btn.grid(column=1, row=19)

while apoapsis_altitude() <= 80000 and Armed == False:

    vessel.auto_pilot.disengage()
    if update_timer == 0:
        window.update()
        update_timer += 0
    else:
        window.update_idletasks()
        update_timer -= 1
    time.sleep(0.1)

while apoapsis_altitude() <= 80000 and Armed == True:

    north = (0, 1, 0)
    east = (0, 0, 1)
    plane_normal = cross(north, east)
    prograde = stream_prograde()
    angle_to_prograde = round(
        math.asin(dot(plane_normal, prograde)) * (180.0/math.pi), 2)
    atmos_dens_abso = round(atmosphere_density(), 5)
    atmos_dens_frac = round(atmos_dens_abso/0.71, 5)
    apoaps_alt = round(apoapsis_altitude(), 2)
    vessel_alt = round(mean_altitude(), 2)

    # ad = 90*((vessel_alt+apoaps_alt)/2/70000)      => sans normalisation atmosphérique
    # => avec normalisation atmosphérique
    ad = 90*(((vessel_alt*atmos_dens_frac) +
              (apoaps_alt*(1-atmos_dens_frac)))/70000)
    # ad = round(vessel.flight().atmosphere_density/0.71,2)
    # vessel.auto_pilot.target_pitch = (90-ad if 90-ad > 0 else angle_to_prograde)
    vessel.auto_pilot.target_pitch = (90-ad if 90-ad > 0 else 0)
    vessel.auto_pilot.target_heading = 90
    vessel.auto_pilot.target_roll = 0
    if apoaps_alt > 80000:
        vessel.control.throttle -= (0.2 if vessel.control.throttle >= 0 else 0)
    elif apoaps_alt <= 80000:
        vessel.control.throttle += (0.2 if vessel.control.throttle <= 1 else 0)
    # print("---------------------------------------------------------------------")
    # print("target alt = ",round((vessel_alt*atmos_dens_frac)+(apoaps_alt*(1-atmos_dens_frac)),2),"m target pitch = ",vessel.auto_pilot.target_pitch,"° Prograde = ",angle_to_prograde)
    # print("Vessel alt norm = ",vessel_alt*atmos_dens_frac,"m,  Apoapsis alt norm = ",apoaps_alt*(1-atmos_dens_frac),"m")
    # print("Vessel alt = ",vessel_alt,"m,  Apoapsis alt= ",apoaps_alt,"m, cible : ",90-ad,"°")
    # print("erreur : ",vessel.auto_pilot.pitch_error,"° Fraction de pression = ",atmos_dens_frac)
    # print('Vertical V:{:03.2f}   PID returns:{:03.2f}   Throttle:{:03.2f}'.format(telem.vertical_speed,pids_output,vessel.control.throttle))

    # the_pids_output=p.update(telem.vertical_speed)
    # v.control.throttle=the_pids_output
    # SMA 20.6031 Mm
    print("DEBUG, throttle, TV", throttle(),
          terminal_velocity(), vessel.flight().terminal_velocity)
    variable_G.set(str(round(g_force(), 2)))
    variable_Ga.set(str(round(g_force()*9.807, 2)))
    variable_Q.set(str(round(dynamic_pressure(), 2)))
    variable_ISP.set(str(round(specific_impulse(), 2)))
    variable_TV.set(str(round(terminal_velocity(), 2)))
    variable_AT.set(str(round((available_thrust()/1000), 2)))
    variable_T.set(str(round((thrust()/1000), 2)))
    variable_TP.set(str(round((throttle()*100), 2)))
    variable_temps.set(str(round(temps, 2)))
    variable_ATP.set(str(round(angle_to_prograde, 2)))
    variable_ADF.set(str(round(atmos_dens_frac, 2)))
    variable_AA.set(str(round(apoaps_alt, 2)))
    variable_VA.set(str(round(vessel_alt, 2)))
    variable_AC.set(str(round((vessel_alt*atmos_dens_frac) +
                              (apoaps_alt*(1-atmos_dens_frac)), 2)))
    # VO = getposition(vessel_direction())
    # variable_Heading.set(str(round(VO[0],2)))
    # variable_Pitch.set(str(round(VO[1],2)))
    # variable_Roll.set(str(round(180+VO[2],2)))

    if update_timer == 0:
        window.update()
        update_timer += 0
    else:
        window.update_idletasks()
        update_timer -= 1
    # print("frameupdate : launched")
    temps += (round(0.0, 3) if notlaunched == False else 0)
    time.sleep(round(0.0, 3))

print("Altitude atteinte")
vessel.auto_pilot.target_pitch = 0
time.sleep(1)
vessel.auto_pilot.disengage()
print("Gravity Turn terminé")

# (((Vang•40000)/(Tracking•sginature))^2 + (max(0,distance-optimal)/fallof)^2)

# ((base_shield_hp*(1/(1-((EM_shield_resist+Therm_shield_resist+Kinetic_shield_resist+Explo_shield_resist)/4)))+base_armor_hp*(1/(1-((EM_armor_resist+Therm_armor_resist+Kinetic_armor_resist+Explo_armor_resist)/4)))+base_hull_hp*(1/(1-((EM_hull_resist+Therm_hull_resist+Kinetic_hull_resist+Explo_hull_resist)/4))))/(1-(speed/(2*pi*orbit_radius))/sig_size))
