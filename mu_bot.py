import pyautogui
import time

# --- CONFIG ---
TEMPO_PARA_UPAR = 20
DELAY_POS_RESET = 5

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

try:
    while True:

        # UPAR
        print("[*] Upando...")
        time.sleep(TEMPO_PARA_UPAR)

        for cmd in comandos_upar:
            enviar(cmd)

        # TENTAR RESET
        print("[!] Tentando reset...")
        enviar("/reset")

        # espera resposta do server
        time.sleep(2)

        # AQUI É A LÓGICA:
        # sempre que tenta reset → considera novo ciclo
        print("[*] Aguardando possível respawn...")
        time.sleep(DELAY_POS_RESET)

        # aplica sobrevivência UMA vez por tentativa de reset
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