from picamera2 import Picamera2
import subprocess
import time

camera_info_list = Picamera2.global_camera_info()
num_cams = len(camera_info_list)

def generate_cmd(cam_index, nominal_frame_rate, file_name, role, duration):
    
    if role not in ("client", "server"):
        raise ValueError("Role must be 'client' or 'server'")
    if duration <= 0:
        raise ValueError("Duration must be longer than 0s")
    if cam_index >= num_cams:
        raise ValueError(f"Only {num_cams} camera(s) detected on the RPi 5.")
    
    # assume that the nominal frame rate is less than the max fps for all cams
    # if this is not true, syncing won't happen properly

    cmd = [
        "rpicam-vid",
        "-n",                                             # no preview window
        "-t", f"{duration}s",
        "--camera", str(cam_index),
        "--framerate", str(nominal_frame_rate),
        "--sync", role,
        "-o", file_name
        ]

    return cmd

client_cmd = generate_cmd(cam_index=1, nominal_frame_rate=30, file_name="client.mp4", role="client", duration=10)
server_cmd = generate_cmd(cam_index=0, nominal_frame_rate=30, file_name="server.mp4", role="server", duration=10)

client_proc = subprocess.Popen(client_cmd)
time.sleep(0.5)
server_proc = subprocess.Popen(server_cmd)
# Wait for both processes to finish
client_proc.wait()
server_proc.wait()
print("Both recordings finished.")