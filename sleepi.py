import RPi.GPIO as GPIO
import logging
import time

green = {'led': 23, 'time': 7, 'debug': 30}
red = {'led': 18, 'time': 6, 'debug': 24}
debug = False

def toggle_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    return

def toggle_off(pin):
    GPIO.output(pin, GPIO.LOW)
    return

def alert():
    toggle_on(green['led'])
    toggle_on(red['led'])
    time.sleep(2)
    toggle_off(green['led'])
    toggle_off(red['led'])
    return

def setup_pi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup((green['led'], red['led']), GPIO.OUT, initial=GPIO.LOW)
    alert()
    return

def diagnostics(lt):
    print "Debugging: ", lt
    pass

def main():
    while True:
        localtime = time.localtime(time.time())
        minute = localtime[4]
        hour = localtime[3]
        if (hour >= red['time'] and minute >= 30) and hour < green['time']:
            toggle_on(red['led'])
            toggle_off(green['led'])
        elif hour >= green['time'] and hour < 8:
            toggle_on(green['led'])
            toggle_off(red['led'])
        else:
            toggle_off(green['led'])
            toggle_off(red['led'])

        if debug:
            diagnostics(localtime)

        time.sleep(600)
        if debug:
            alert
def shutdown_pi():
    GPIO.cleanup()
    return

def run_diagnostics():
    print "Running diagnostics..."
    tick = 0
    lower = 6
    upper = 7
    while tick < 10:
        print "tick: ", tick
        if tick >= lower and tick < upper:
            print "enabling red"
            toggle_on(red['led'])
            toggle_off(green['led'])
        elif tick >= upper and tick < 8:
            print "enabling green"
            toggle_on(green['led'])
            toggle_off(red['led'])
        else:
            print "disabled both"
            toggle_off(green['led'])
            toggle_off(red['led'])
        time.sleep(1)
        tick += 1

if __name__ == "__main__":
    setup_pi()
    try:
        if debug:
            run_diagnostics()
        main()
    except:
        pass
    finally:
        shutdown_pi()
