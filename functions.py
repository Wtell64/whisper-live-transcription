from pydub import AudioSegment
import whisper
import os
import sounddevice as sd
import wave
import numpy as np

def combineWavFiles(wav1,wav2):
    sound1 = AudioSegment.from_wav(wav1)
    sound2 = AudioSegment.from_wav(wav2)
    combined_sounds = sound1 + sound2
    combined_sounds.export("./combined_recording/combined.wav", format="wav")


def compareList(list1, list2):
    
    # Convert the lists to sets
    set1 = set(list1)
    set2 = set(list2)

    # Find the different elements using set operations
    different_elements = set1.symmetric_difference(set2)

    # Convert the result back to a list
    return sorted(list(different_elements), reverse = False)

def translateModel(model, file):
        audio = whisper.load_audio(file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        options = whisper.DecodingOptions(language= 'en', fp16=False)

        return whisper.decode(model, mel, options)
    
def checkStringInList(given_string, string_list):
    if given_string in string_list:
        return True
    else:
        return False
    
def delete_files_in_folder(folder_paths):
    # Get the list of files in the folder
    for folder in folder_paths:
    
        files = os.listdir(folder)
        
        # Check if the folder is empty
        if len(files) == 0:
            print("Folder is empty. No files to delete.")
            return
        
        # Delete each file in the folder
        for file in files:
            file_path = os.path.join(folder, file)
            os.remove(file_path)
        print(f"Previous files deleted in {folder}")

def record_audio(duration, filename, foldername, new_session):
    i = 1
    fs = 44100  # Sample rate (Hz)
    
    if new_session: # If we want to delete old recording files
        delete_files_in_folder(foldername)
        
    while True:
        
        currentfilename = f"{filename}_{i}.wav"
        

        # Record audio
        print("Recording audio...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        # Normalize and convert the recorded audio to 16-bit integers
        normalized_audio = np.int16(recording / np.max(np.abs(recording)) * 32767)

        # Save the recorded audio to a WAV file
        with wave.open(currentfilename, "wb") as file:
            file.setnchannels(1)  # Mono
            file.setsampwidth(2)  # 16 bits
            file.setframerate(fs)
            file.writeframes(normalized_audio.tobytes())

        print(f"Recording saved as {currentfilename}")
        
        i += 1

def remove_string_from_list(list, string):
    return [element for element in list if element != string]

def create_folders(create_folders_flag):
    if create_folders_flag:
        folder_names = ["combined_recording", "recordings", "transcribe"]
        current_directory = os.getcwd()

        for folder_name in folder_names:
            folder_path = os.path.join(current_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)

        print("Folders for storing the recordings created successfully.")
    else:
        print("No folders were created.")


