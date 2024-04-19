import cv2

# Inicializa la cámara
cap = cv2.VideoCapture(0)  # 0 es generalmente el índice de la primera cámara

# Revisa si la cámara se inició correctamente
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

try:
    while True:
        # Captura frame-por-frame
        ret, frame = cap.read()

        # Si frame se lee correctamente ret es True
        if not ret:
            print("No se pudo leer el frame...")
            break

        # Muestra el frame resultante
        cv2.imshow('Camara', frame)

        # Presiona 'q' para salir
        if cv2.waitKey(1) == ord('q'):
            break
finally:
    # Cuando todo esté hecho, libera la captura
    cap.release()
    cv2.destroyAllWindows()
