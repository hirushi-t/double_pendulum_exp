from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time

# works well!
# may need different ISO and shutter speed settings for global shutter camera


def record_video(video_length, width, height, fps, camera_num, filename, file_type):
    '''
    Args:

    '''
    try:
        # create an instance of the Picamera2 class
        # basically, initialising the camera
        picam2 = Picamera2(camera_num=camera_num)

        # choosing right settings
        video_config = picam2.create_video_configuration(
            main={"size": (width, height)}, 
            controls={"FrameRate": fps}
        )

        # apply config to camera we initialised
        picam2.configure(video_config)

        # mimic original ISO and shutter_speed settings
        picam2.set_controls({
            #"Ae": False,     # disable auto-exposure
            "AnalogueGain": 8.0,       # sensitivity for light --> AG x 100 = ISO
            "ExposureTime": 1500       # Shutter speed --> exposed to light for 1500 microsecs
        })

        time.sleep(2.1)                # give camera time to adjust
        
        encoder = H264Encoder()        # used to compress the raw vid
        output = filename + file_type

        # start recording
        picam2.start_recording(encoder=encoder, output=output)
        time.sleep(video_length)
        picam2.stop_recording()

    except Exception as e:
        print(e)
        
        
record_video(10,640,480,30,1,"record_vid_test_IR", ".h264")  