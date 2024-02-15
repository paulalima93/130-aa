import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller
import pyautogui
keyboard = Controller()

cap = cv2.VideoCapture(0)

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]


# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):

    if hand_landmarks:
        # Obtenha todos os marcos da PRIMEIRA Mão VISÍVEL
        landmarks = hand_landmarks[handNo].landmark

        # Conte os dedos        
        fingers = []

        for lm_index in tipIds:
                # Obtenha os valores y da ponta e da parte inferior do dedo
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Verifique se ALGUM DEDO está ABERTO ou FECHADO
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("DEDO com id ",lm_index," is Open")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("DEDO com id ",lm_index," is Closed")

        totalFingers = fingers.count(1)
        
        # REPRODUZIR ou PAUSAR O vídeo
        if totalFingers == 4:
            state = "Play"

        if totalFingers == 0 and state == "Play":
            state = "Pause"
            keyboard.press("k")
 
        ################################

             # ADICIONE O CÓDIGO AQUI #

        ################################ 

# Definir uma função para 
def drawHandLanmarks(image, hand_landmarks):

    # Desenhe conexões entre pontos de referência
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detectar os pontos de referência das mãos 
    results = hands.process(image)

    # Obter a posição do ponto de referência a partir do resultado processado
    hand_landmarks = results.multi_hand_landmarks

    # Desenhar pontos de referência
    drawHandLanmarks(image, hand_landmarks)

    # Obter posição dos dedos das mãos        
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de Mídia", image)

    # Saia da janela ao pressionar a tecla barra de espaço
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
