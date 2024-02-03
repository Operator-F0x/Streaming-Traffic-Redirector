# RST Streaming Traffic Redirector

import os
import subprocess
import threading

def print_error(message):
    print(f"Error: {message}")

def print_success(message):
    print(f"Success: {message}")

def process_m3u_files(input_folder, output_folder):
    try:
        # Find all .m3u files in the input folder
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

                    # Simulate streaming from {url} to http://127.0.0.1:8311/{stream_url}
                    print(f"Streaming from {url} to http://127.0.0.1:8311/{stream_url}")

                    # Write the URL to the output file
                    with open(output_path, 'a') as output_file:
                        output_file.write(f'#EXTINF:-1,{url}\nhttp://127.0.0.1:8311/{stream_url}\n')

                    print_success(f"Streaming completed for: {url}")

                    stream_counter += 1

                # Start ffmpeg in a separate thread
                thread = threading.Thread(target=start_ffmpeg, args=(input_path,))
                thread.start()

    except FileNotFoundError:
        print_error(f"Input folder not found: {input_folder}")
    except PermissionError:
        print_error(f"Insufficient permissions to open the input folder: {input_folder}")

def start_ffmpeg(input_path):
    output_url = "http://127.0.0.1:8311/stream"
    ffmpeg_command = f'ffmpeg -re -i {input_path} -c copy -f mpegts {output_url}'
    subprocess.run(ffmpeg_command, shell=True)

def create_folders(output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Output folder created: {output_folder}")

def main():
    input_folder = 'trackstrem/m3u'
    output_folder = 'trackstrem/output/stream_output'

    create_folders(output_folder)

    process_m3u_files(input_folder, output_folder)

    print_success("Processing completed.")

if __name__ == "__main__":
    main()
