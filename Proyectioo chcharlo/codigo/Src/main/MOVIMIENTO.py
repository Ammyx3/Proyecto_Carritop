import RPi.GPIO as GPIO
import time

# ── Pines ──────────────────────────────────────────────
IN1, IN2, EN1 = 17, 18, 22   # Motor A
IN3, IN4, EN2 = 23, 24, 25   # Motor B
PWM_FREQ = 1000               # Hz

# ── Inicialización ─────────────────────────────────────
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in (IN1, IN2, EN1, IN3, IN4, EN2):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

pwm_a = GPIO.PWM(EN1, PWM_FREQ)
pwm_b = GPIO.PWM(EN2, PWM_FREQ)
pwm_a.start(0)
pwm_b.start(0)

# ── Primitivas ─────────────────────────────────────────
def _motor_a(direccion, vel):
    GPIO.output(IN1, GPIO.HIGH if direccion == "adelante" else GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW  if direccion == "adelante" else GPIO.HIGH)
    pwm_a.ChangeDutyCycle(vel)

def _motor_b(direccion, vel):
    GPIO.output(IN3, GPIO.HIGH if direccion == "adelante" else GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW  if direccion == "adelante" else GPIO.HIGH)
    pwm_b.ChangeDutyCycle(vel)

def _stop_a():
    GPIO.output(IN1, GPIO.LOW); GPIO.output(IN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)

def _stop_b():
    GPIO.output(IN3, GPIO.LOW); GPIO.output(IN4, GPIO.LOW)
    pwm_b.ChangeDutyCycle(0)

def detener():
    _stop_a(); _stop_b()

def limpiar():
    detener(); pwm_a.stop(); pwm_b.stop(); GPIO.cleanup()

# ── Secuencia ──────────────────────────────────────────
def ejecutar_secuencia(vel=75):
    """
    Ejecuta la secuencia completa de movimientos.
    vel: velocidad general 0-100 (%).
    """

    # ── Paso 1: Ambos adelante 3 s ─────────────────────
    print("[ 1/6 ] Ambos motores → ADELANTE (3 s)")
    _motor_a("adelante", vel)
    _motor_b("adelante", vel)
    time.sleep(3)
    detener()
    time.sleep(0.3)

    # ── Paso 2: Ambos atrás 3 s ────────────────────────
    print("[ 2/6 ] Ambos motores → ATRÁS (3 s)")
    _motor_a("atras", vel)
    _motor_b("atras", vel)
    time.sleep(3)
    detener()
    time.sleep(0.3)

    # ── Paso 3: Gira solo motor A (2 s) → ambos adelante
    print("[ 3/6 ] Solo Motor A gira (2 s)  →  ambos ADELANTE")
    _motor_a("adelante", vel)   # solo A
    _stop_b()                   # B parado → robot pivota sobre B
    time.sleep(2)

    # Continúa: ambos adelante sin pausa intermedia
    _motor_b("adelante", vel)
    print("         Ambos adelante (3 s)")
    time.sleep(3)
    detener()
    time.sleep(0.3)

    # ── Paso 4: Gira solo motor B (2 s) → ambos atrás ─
    print("[ 4/6 ] Solo Motor B gira (2 s)  →  ambos ATRÁS")
    _motor_b("adelante", vel)   # solo B
    _stop_a()                   # A parado → robot pivota sobre A
    time.sleep(2)

    # Continúa: ambos atrás sin pausa intermedia
    _motor_a("atras", vel)
    _motor_b("atras", vel)
    print("         Ambos atrás (3 s)")
    time.sleep(3)
    detener()
    time.sleep(0.3)

    # ── Paso 5a: Motor A adelante / Motor B atrás (3 s) ─
    print("[ 5/6 ] Motor A → ADELANTE  |  Motor B → ATRÁS (3 s)")
    _motor_a("adelante", vel)
    _motor_b("atras",    vel)
    time.sleep(3)
    detener()
    time.sleep(0.3)

    # ── Paso 6: Inversión → Motor A atrás / Motor B adelante (3 s)
    print("[ 6/6 ] Motor A → ATRÁS  |  Motor B → ADELANTE  [inversión] (3 s)")
    _motor_a("atras",    vel)
    _motor_b("adelante", vel)
    time.sleep(3)

    detener()
    print("\n✔  Secuencia completada.")


# ── Punto de entrada ───────────────────────────────────
if __name__ == "__main__":
    try:
        print("=== Secuencia de motores L293D ===\n")
        ejecutar_secuencia(vel=75)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    finally:
        limpiar()
        print("GPIO liberado.")