import cv2 
import mediapipe as mp

# Inicializo la cámara (0 para la cámara principal)
cap = cv2.VideoCapture(0) 

# Cargo el modelo de detección de manos y las herramientas de dibujo
mp_manos = mp.solutions.hands 
mp_dibujo = mp.solutions.drawing_utils 

# Inicializo el detector de manos con parámetros de confianza
manos = mp_manos.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) 

while True:
    # Capturo un fotograma de la cámara
    ret, frame = cap.read()  # 'ret' indica si la captura fue exitosa, 'frame' contiene la imagen
    if not ret:
        break  # Si la captura falla, salir del bucle

    # Convierto la imagen de BGR a RGB, ya que MediaPipe trabaja con RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

    # Proceso la imagen con MediaPipe para detectar manos
    results = manos.process(rgb_frame) 

    # Verifico si se detectó al menos una mano
    if results.multi_hand_landmarks: 
        for hand_landmarks in results.multi_hand_landmarks:  # Recorro todas las manos detectadas
            # Dibujo los puntos clave y conexiones de la mano detectada
            mp_dibujo.draw_landmarks(frame, hand_landmarks, mp_manos.HAND_CONNECTIONS) 
            
            # Obtengo los puntos clave de la mano detectada
            landmarks = hand_landmarks.landmark 

            dedos_abiertos = 0  # Contador de dedos abiertos
            dedos_ids = [4, 8, 12, 16, 20]  # IDs de las puntas de los dedos

            # Reviso los dedos (excepto el pulgar)
            for i in dedos_ids[1:]:  
                # Si la punta del dedo está por encima del nudillo, lo considero abierto
                if landmarks[i].y < landmarks[i - 2].y: 
                    dedos_abiertos += 1 
            
            # Lógica para detectar si el pulgar está extendido (se mueve en el eje X)
            if landmarks[4].x > landmarks[3].x:  
                dedos_abiertos += 1  
            
            # Determino el estado de la mano y el color del texto
            if dedos_abiertos >= 4:
                estado_mano = "Mano Abierta"
                color_texto = (0, 255, 0)  # Verde
            else:
                estado_mano = "Mano Cerrada"
                color_texto = (0, 0, 255)  # Rojo
            
            # Muestro el estado de la mano en la imagen
            cv2.putText(frame, estado_mano, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color_texto, 2)
    
    
    # Muestro la imagen procesada en una ventana
    cv2.imshow("Detección de Manos", frame)
    
    # Si se presiona la tecla 'Esc', salir del bucle
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libero la cámara y cierro las ventanas
cap.release()
cv2.destroyAllWindows()
