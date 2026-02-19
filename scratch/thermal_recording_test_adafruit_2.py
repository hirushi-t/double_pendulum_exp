import time
import board
import busio
import adafruit_mlx90640

# have to run this from the virtual environment dp_exp
# because adafruit module is only installed here

def record_thermal_data(duration_seconds):
    error_count = 0

    i2c = busio.I2C(board.SCL, board.SDA)
    mlx = adafruit_mlx90640.MLX90640(i2c)

    # Set refresh rate (frames per second)
    # Keep increasing until you max out
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

    # 1 frame buffer will hold one frame of thermal data
    frame_buffer = [0] * 768
    
    # will store all captured frames
    recorded_frames = []

    # time.motonic gives a continous clock
    start_time = time.monotonic()
    while time.monotonic() - start_time < duration_seconds:
        try:
            mlx.getFrame(frame_buffer)
            recorded_frames.append(frame_buffer.copy())
        except ValueError:
            # Occasionally MLX90640 throws this, just retry
            error_count += 1
            continue
    print(error_count)

    return recorded_frames

# Example usage: record 10 seconds of thermal data
frames = record_thermal_data(10)

print(len(frames[0]))
print("Recorded", len(frames), "frames")

