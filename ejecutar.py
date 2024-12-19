import cv2
from ultralytics import YOLO
import threading

# Configuración
MODEL_PATH = "./runs/detect/train/weights/best.pt"  # Modelo entrenado
CAMERA_URL = "http://192.168.0.69:4747/video"  # URL de DroidCamApp

# Configuración de la resolución (640x640 por defecto en YOLO)
FRAME_WIDTH = 640
FRAME_HEIGHT = 640
FRAME_SKIP = 4  # Procesa un cuadro cada 4

# Variables globales para threading
frame = None
ret = False
stop_thread = False

def camera_reader(cap):
    """
    Lee la cámara en un hilo separado.
    """
    global frame, ret, stop_thread
    while not stop_thread:
        ret, frame = cap.read()

def run_inference():
    print("Cargando modelo YOLO entrenado...")
    model = YOLO(MODEL_PATH)
    print("Tipo de clase: ", model.names)

    print("Conectando a la cámara...")
    cap = cv2.VideoCapture(CAMERA_URL)

    # Configuración de la resolución
    print("Configurando resolución...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("Error: No se puede conectar a la cámara.")
        return

    # Iniciar el hilo de lectura de la cámara
    print("Iniciando lectura de la cámara...")
    camera_thread = threading.Thread(target=camera_reader, args=(cap,))
    camera_thread.start()

    print("Presiona 'q' para salir.")
    frame_count = 0

    try:
        while True:
            if not ret:
                continue  # Si no hay frame disponible, sigue esperando

            # Salta cuadros para ahorrar rendimiento
            if frame_count % FRAME_SKIP == 0:
                results = model(frame)
                annotated_frame = results[0].plot()
                cv2.imshow("Detección en tiempo real", annotated_frame)

            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupción manual detectada. Saliendo...")

    # Detener hilo y liberar recursos
    global stop_thread
    stop_thread = True
    camera_thread.join()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_inference()
