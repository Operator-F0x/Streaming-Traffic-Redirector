import os
import subprocess
import threading

# Utility functions for logging
def log_error(message):
    print(f"[ERROR] {message}")

def log_success(message):
    print(f"[SUCCESS] {message}")

def log_info(message):
    print(f"[INFO] {message}")

# Function to process .m3u files
def process_m3u_files(input_folder, output_folder):
    try:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Find all .m3u files in the input folder
        m3u_files = [f for f in os.listdir(input_folder) if f.endswith('.m3u')]

        if not m3u_files:
            log_info("No .m3u files found in the input folder.")
            return

        for m3u_filename in m3u_files:
            input_path = os.path.join(input_folder, m3u_filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(m3u_filename)[0]}_output.m3u")

            process_single_m3u(input_path, output_path)

    except FileNotFoundError:
        log_error(f"Input folder not found: {input_folder}")
    except PermissionError:
        log_error(f"Insufficient permissions to access the input folder: {input_folder}")

# Function to process a single .m3u file
def process_single_m3u(input_path, output_path):
    try:
        stream_counter = 0

        with open(input_path, 'r') as m3u_file, open(output_path, 'w') as output_file:
            for line in m3u_file:
                if line.startswith('#') or line.strip() == "":
                    continue

                url = line.strip()
                stream_url = f'stream_{stream_counter}'

                # Simulate streaming
                log_info(f"Streaming from {url} to http://127.0.0.1:8311/{stream_url}")

                # Write the URL to the output file
                output_file.write(f'#EXTINF:-1,{url}\nhttp://127.0.0.1:8311/{stream_url}\n')

                log_success(f"Stream added for: {url}")

                stream_counter += 1

        # Start ffmpeg in a separate thread
        threading.Thread(target=start_ffmpeg, args=(input_path,)).start()

    except FileNotFoundError:
        log_error(f"File not found: {input_path}")
    except PermissionError:
        log_error(f"Insufficient permissions to read/write: {input_path} or {output_path}")

# Function to start FFmpeg process
def start_ffmpeg(input_path):
    try:
        output_url = "http://127.0.0.1:8311/stream"
        ffmpeg_command = [
            'ffmpeg', '-re', '-i', input_path, '-c', 'copy', '-f', 'mpegts', output_url
        ]
        log_info(f"Starting FFmpeg with command: {' '.join(ffmpeg_command)}")
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        log_error(f"FFmpeg process failed: {e}")
    except FileNotFoundError:
        log_error("FFmpeg executable not found. Make sure it is installed and in your PATH.")

# Main entry point of the script
def main():
    input_folder = 'trackstrem/m3u'
    output_folder = 'trackstrem/output/stream_output'

    log_info("Starting M3U file processing...")
    process_m3u_files(input_folder, output_folder)
    log_success("All files processed successfully.")

if __name__ == "__main__":
    main()
