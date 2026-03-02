import pyautogui
import time

# --- CONFIG ---
TEMPO_PARA_UPAR = 5
DELAY_POS_RESET = 3

# reset
INTERVALO_RESET = 10 * 60   # 13 minutos

# /a
LIMITE_A = 3800
INCREMENTO_A = 400

# comandos
comandos_loop = ["/f 3000", "/e 6000", "/v 1500"]   # boost inicial
comandos_upar = ["/a 0", "/f 200", "/e 300", "/v 100"]  # ciclos normais

def enviar(cmd):
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.write(cmd, interval=0.03)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.4)

print(">>> BOT AUTO RESET SINCRONIZADO <<<")
print("Clique no MU. Iniciando em 5s...")
time.sleep(5)

valor_a = 0
primeiro_ciclo = True
ultimo_reset = 0

try:
    while True:

        print("[*] Upando...")
        time.sleep(TEMPO_PARA_UPAR)

        agora = time.time()

        # -------- RESET CONTROLADO --------
        if agora - ultimo_reset >= INTERVALO_RESET:
            print("[!] RESET EXECUTADO (16 min)")
            enviar("/reset")
            ultimo_reset = agora

            # 🔥 sincroniza estado com o jogo
            valor_a = 0
            primeiro_ciclo = True

            time.sleep(DELAY_POS_RESET)
        else:
            restante = int(INTERVALO_RESET - (agora - ultimo_reset))
            print(f"[=] Reset bloqueado, faltam {restante}s")

        # -------- /A INCREMENTAL --------
        if valor_a < LIMITE_A:
            incremento = min(INCREMENTO_A, LIMITE_A - valor_a)
            valor_a += incremento
            print(f"[+] Incrementando /a em +{incremento} → total {valor_a}")
            enviar(f"/a {incremento}")
        else:
            print("[=] /a no limite (3800). Ignorado.")

        # -------- PONTOS --------
        if primeiro_ciclo:
            print("[+] Primeiro ciclo pós-reset: boost inicial")
            for cmd in comandos_loop:
                enviar(cmd)
            primeiro_ciclo = False
        else:
            print("[+] Ciclo normal: upar padrão")
            for cmd in comandos_upar:
                if cmd.startswith("/a"):  # /a já é controlado acima
                    continue
                enviar(cmd)

        enviar("/zen")

except KeyboardInterrupt:
    print("\n[!] Script encerrado.")
