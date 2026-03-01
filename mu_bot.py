import pyautogui
import time

# --- CONFIG ---
TEMPO_PARA_UPAR = 5
DELAY_POS_RESET = 3
TEMPO_ENTRE_RESETS = 360  # ⏱️ 6 minutos (360 segundos)

comandos_sobrevivencia = ["/a 1400", "/f 1000", "/e 4000", "/v 500"]
comandos_upar = ["/a 0", "/f 200", "/e 300", "/v 100"]

def enviar(cmd):
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.write(cmd, interval=0.03)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.4)

print(">>> BOT AUTO RESET SIMPLES <<<")
print("Clique no MU. Iniciando em 5s...")
time.sleep(5)

ja_aplicou_sobrevivencia = False
ultimo_reset = 0  # marca tempo do último reset

try:
    while True:

        # UPAR
        print("[*] Upando...")
        time.sleep(TEMPO_PARA_UPAR)

        for cmd in comandos_upar:
            enviar(cmd)

        # CONTROLE DE TEMPO (6 MINUTOS)
        agora = time.time()
        if agora - ultimo_reset < TEMPO_ENTRE_RESETS:
            restante = int(TEMPO_ENTRE_RESETS - (agora - ultimo_reset))
            print(f"[*] Aguardando {restante}s para próximo reset...")
            time.sleep(5)
            continue

        # RESET
        print("[!] Tentando reset...")
        enviar("/reset")
        ultimo_reset = time.time()  # marca horário do reset

        # espera resposta do server
        time.sleep(2)

        print("[*] Aguardando possível respawn...")
        time.sleep(DELAY_POS_RESET)

        # aplica sobrevivência UMA vez por reset
        if not ja_aplicou_sobrevivencia:
            print("[+] Aplicando sobrevivência pós-reset...")
            for cmd in comandos_sobrevivencia:
                enviar(cmd)
            ja_aplicou_sobrevivencia = True

        enviar("/zen")

        # libera próximo ciclo
        ja_aplicou_sobrevivencia = False

except KeyboardInterrupt:
    print("\n[!] Script encerrado.")
