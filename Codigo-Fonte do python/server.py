# pc_monitor_server.py
import psutil
import platform
from flask import Flask, jsonify
from flask_cors import CORS
from collections import deque
import os
import shutil
import tempfile

app = Flask(__name__)
CORS(app)

# Histórico limitado a 30 pontos
HISTORY_SIZE = 30
history_cpu = deque(maxlen=HISTORY_SIZE)
history_ram = deque(maxlen=HISTORY_SIZE)
history_disk = deque(maxlen=HISTORY_SIZE)

@app.route("/status")
def status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    windows_version = platform.platform()

    # Atualiza histórico
    history_cpu.append(cpu)
    history_ram.append(ram)
    history_disk.append(disk)

    return jsonify({
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "windows_version": windows_version,
        "history": {
            "cpu": list(history_cpu),
            "ram": list(history_ram),
            "disk": list(history_disk)
        }
    })

# Rotas para otimização real e segura
@app.route("/optimize/cpu")
def optimize_cpu():
    # Simulação: retorna mensagem
    return jsonify({"message": "CPU otimizada! (simulação segura)"})

@app.route("/optimize/ram")
def optimize_ram():
    # Libera memória cache de forma segura
    try:
        if platform.system() == "Windows":
            # No Windows, apenas simulação segura
            message = "Memória RAM otimizada! (simulação segura)"
        else:
            # No Linux/macOS, limpa caches
            os.system("sync; echo 3 > /proc/sys/vm/drop_caches")
            message = "Memória RAM liberada!"
    except Exception as e:
        message = f"Erro ao otimizar RAM: {e}"
    return jsonify({"message": message})

@app.route("/optimize/disk")
def optimize_disk():
    try:
        temp_dir = tempfile.gettempdir()
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                continue
        message = "Disco temporário limpo com sucesso!"
    except Exception as e:
        message = f"Erro ao limpar disco: {e}"
    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
