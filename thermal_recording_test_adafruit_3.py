import time
import board
import busio
import adafruit_mlx90640

# same as recording_thermal_vid_2 but now also records timestamps

def record_thermal_data(duration_seconds):
    error_count = 0

    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90640.MLX90640(i2c)

    # Set refresh rate
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

    frame_buffer = [0] * 768
    recorded_frames = []
    frame_times = []  # <-- new list to store timestamps

    start_time = time.monotonic()
    while time.monotonic() - start_time < duration_seconds:
        try:
            mlx.getFrame(frame_buffer)
            recorded_frames.append(frame_buffer.copy())
            frame_times.append(time.monotonic() - start_time)
        except ValueError:
            error_count += 1
            continue

    print("Number of read errors:", error_count)
    return recorded_frames, frame_times

# Record 10 seconds of thermal data
frames, times = record_thermal_data(10)

print("Pixels per frame:", len(frames[0]))
print("Number of frames recorded:", len(frames))
print("Timestamps for first 5 frames:", times[:5])

