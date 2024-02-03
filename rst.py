#RST Streaming Traffic Redirecter

import os
import subprocess
import threading

def print_error(message):
    print(f"Errore: {message}")

def print_success(message):
    print(f"Successo: {message}")

def process_m3u_files(input_folder, output_folder):
    try:
        # Trova tutti i file .m3u nella cartella di input
        m3u_files = [f for f in os.listdir(input_folder) if f.endswith('.m3u')]

        for m3u_filename in m3u_files:
            input_path = os.path.join(input_folder, m3u_filename)
            output_path = os.path.join(output_folder, f"{m3u_filename.split('.')[0]}_output.m3u")

            with open(input_path, 'r') as m3u_file:
                stream_counter = 0

                for line in m3u_file:
                    if line.startswith('#') or line.isspace():
                        continue

                    url = line.strip()
                    stream_url = f'stream_{stream_counter}'

                    # Simulazione della trasmissione del flusso
                    print(f"Trasmissione del flusso da {url} a http://127.0.0.1:8311/{stream_url}")

                    # Avvia ffmpeg in un thread separato
                    thread = threading.Thread(target=start_ffmpeg, args=(url, stream_url))
                    thread.start()

                    # Scrivi l'URL nel file di output
                    with open(output_path, 'a') as output_file:
                        output_file.write(f'#EXTINF:-1,{url}\nhttp://127.0.0.1:8311/{stream_url}\n')

                    print_success(f"Trasmissione completata per: {url}")

                    stream_counter += 1

    except FileNotFoundError:
        print_error(f"Cartella di input non trovata: {input_folder}")
    except PermissionError:
        print_error(f"Permessi insufficienti per aprire la cartella di input: {input_folder}")

def start_ffmpeg(input_url, stream_url):
    ffmpeg_command = f'ffmpeg -re -i {input_url} -c copy -f mpegts http://127.0.0.1:8311/{stream_url}'
    subprocess.run(ffmpeg_command, shell=True)

def create_folders(output_folder):
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Cartella di output creata: {output_folder}")

def main():
    input_folder = 'trackstrem/m3u'
    output_folder = 'trackstrem/output/stream_output'

    create_folders(output_folder)

    process_m3u_files(input_folder, output_folder)

    print_success("Elaborazione completata.")

if __name__ == "__main__":
    main()
