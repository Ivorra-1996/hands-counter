import cv2
from ultralytics import YOLO

# Configuración
MODEL_PATH = "./runs/detect/train/weights/best.pt"  # Modelo entrenado
CAMERA_URL = "http://192.168.0.69:4747/video"  # URL de DroidCamApp

# Configuración de la resolución (640x640 por defecto en YOLO)
FRAME_WIDTH = 640
FRAME_HEIGHT = 640

def run_inference():
    frame_skip : int = 4  # Procesa un cuadro cada 4
    frame_count : int = 0

    print("Cargando modelo YOLO entrenado...")
    model = YOLO(MODEL_PATH)
    print("Tipo de clase: ", model.names)

    print("Conectando a la cámara...")
    cap = cv2.VideoCapture(CAMERA_URL)

    print("Configurando resolución...")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)


    if not cap.isOpened():
        print("Error: No se puede conectar a la cámara.")
        return

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Salta cuadros 
        if frame_count % frame_skip == 0:
            results = model(frame)
            annotated_frame = results[0].plot()
            cv2.imshow("Detección en tiempo real", annotated_frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_inference()