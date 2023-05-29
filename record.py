if __name__ == "__main__":

    import sounddevice as sd
    import numpy as np
    import wave
    import whisper
    import os
    from functions import *


    ######################### Define Variables #########################
    model = whisper.load_model("base")
    duration = 3
    i = 1
    new_session = False
    foldername = ["./recordings","./combined_recording","./transcriptions"]
    filename = "recordings/recording"
    ######################### Run the Function #########################

    record_audio(duration, filename, foldername ,new_session)





