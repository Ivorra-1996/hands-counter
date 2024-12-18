import cv2
from ultralytics import YOLO

# Configuración
MODEL_PATH = "./runs/detect/train/weights/best.pt"  # Modelo entrenado
CAMERA_URL = "http://192.168.0.100:4747/video"  # URL de DroidCamApp

def run_inference():
    print("Cargando modelo YOLO entrenado...")
    model = YOLO(MODEL_PATH)
    
    print("Conectando a la cámara...")
    cap = cv2.VideoCapture(CAMERA_URL)

    if not cap.isOpened():
        print("Error: No se puede conectar a la cámara.")
        return

    print("Presiona 'q' para salir.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Realizar inferencia
        results = model(frame)

        # Mostrar resultados en pantalla
        annotated_frame = results[0].plot()
        cv2.imshow("Detección en tiempo real", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_inference()