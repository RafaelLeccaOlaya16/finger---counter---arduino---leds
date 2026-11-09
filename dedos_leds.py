import cv2
import mediapipe as mp
import serial
import time
puerto = "COM5"
velocidad = 9600
arduino = serial.Serial(puerto, velocidad, timeout=1)
time.sleep(2)
modulo_manos = mp.solutions.hands
detector_de_manos = modulo_manos.Hands(max_num_hands=1,
                                       min_detection_confidence=0.7,
                                       min_tracking_confidence=0.7)
camara = cv2.VideoCapture(0)
while True:
    funciono, foto = camara.read()
    if funciono == False:
        break
    foto = cv2.flip(foto, 1)
    foto_en_rojo_verde_azul = cv2.cvtColor(foto, cv2.COLOR_BGR2RGB)
    resultado = detector_de_manos.process(foto_en_rojo_verde_azul)
    pulgar = 0
    indice = 0
    medio = 0
    anular = 0
    menique = 0
    if resultado.multi_hand_landmarks != None:
        mano = resultado.multi_hand_landmarks[0]
        puntos = mano.landmark
        x_punta_pulgar = puntos[4].x
        x_articulacion_pulgar = puntos[3].x
        x_base_menique = puntos[17].x
        distancia_punta = x_punta_pulgar - x_base_menique
        if distancia_punta < 0:
            distancia_punta = distancia_punta * -1
        distancia_articulacion = x_articulacion_pulgar - x_base_menique
        if distancia_articulacion < 0:
            distancia_articulacion = distancia_articulacion * -1
        if distancia_punta > distancia_articulacion:
            pulgar = 1
        y_punta_indice = puntos[8].y
        y_articulacion_indice = puntos[6].y
        if y_punta_indice < y_articulacion_indice:
            indice = 1
        y_punta_medio = puntos[12].y
        y_articulacion_medio = puntos[10].y
        if y_punta_medio < y_articulacion_medio:
            medio = 1
        y_punta_anular = puntos[16].y
        y_articulacion_anular = puntos[14].y
        if y_punta_anular < y_articulacion_anular:
            anular = 1
        y_punta_menique = puntos[20].y
        y_articulacion_menique = puntos[18].y
        if y_punta_menique < y_articulacion_menique:
            menique = 1
    mensaje = str(pulgar) + str(indice) + str(medio) + str(anular) + str(menique)
    texto_con_espacio = mensaje + "\n"
    arduino.write(texto_con_espacio.encode())

    cv2.imshow("Camara", foto)

    tecla = cv2.waitKey(1)
    if tecla == ord("e"):
        break

camara.release()
arduino.close()
cv2.destroyAllWindows()