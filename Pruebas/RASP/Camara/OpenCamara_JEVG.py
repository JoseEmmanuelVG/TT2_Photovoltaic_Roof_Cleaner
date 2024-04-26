import cv2
from picamera2 import Picamera2
from time import sleep

def main():
    picam2 = Picamera2()
    picam2.start_preview(fullscreen=False, window=(0, 0, 640, 480))

    # Configura la cámara para una resolución baja para visualización en tiempo real
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()

    try:
        while True:
            # Captura un frame
            frame = picam2.capture_array()
            # Muestra el frame
            cv2.imshow('Camera', frame)
            # Espera por la tecla 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Asegura que la cámara se detenga y cierra las ventanas de OpenCV
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
