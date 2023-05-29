if __name__ == "__main__":

    import whisper
    import os, glob
    from pydub import AudioSegment
    from functions import *
    import shutil


    print("Translate Program Started!")

    transcribed = []
    i = 1
    recordings_dir = os.path.join('recordings', '*')
    previous_files = []
    combine_file = './combined_recording/combined.wav'

    print("Creating folders to store the recordings and trascription files")
    
    create_folders(True)

    print("Deleting Old Folders")
    
    delete_files_in_folder(["./recordings","./combined_recording","./transcriptions"])

    print("Loading the Model")

    model = whisper.load_model("small")

    print("Waiting for a recording")
    while True:
        
        current_files = sorted(glob.iglob(recordings_dir), key=os.path.getctime, reverse=True)
        
        latest_file_path = f"transcriptions/transcript_{i}"
        latest_file_name = f"transcript_{i}"
        
        comparedfiles = compareList(current_files, previous_files)
        
        if (len(current_files) == 1 and not latest_file_name in  transcribed and i == 1):

            combined_recording = current_files[0]

            result = translateModel(model, combined_recording)
            
            if result.no_speech_prob < 0.8:


                print(result.text)

                # append text to transcript file
                with open(latest_file_path, 'a') as f:
                    f.write(result.text)
                    
                i += 1
                #  os.system('cls' if os.name == 'nt' else 'clear')
                # save list of transcribed recordings so that we don't transcribe the same one again
                transcribed.append(latest_file_path)

                shutil.copy(combined_recording,combine_file)
                

            continue
        

        #chech if file one is not there. Same transcribe is not happening
        if len(current_files) >= 2 and len(comparedfiles) != 0:

            comparedfiles = remove_string_from_list(comparedfiles,"recordings\\recording_1.wav")
            
            for file in comparedfiles:
                combineWavFiles(combine_file,file)
                
            
            result = translateModel(model, combine_file)

            if result.no_speech_prob < 0.8:
                
                print(result.text)

                # append text to transcript file
                with open(latest_file_path, 'a') as f:
                    f.write(result.text)
                    
                i += 1
                #  os.system('cls' if os.name == 'nt' else 'clear')
                # save list of transcribed recordings so that we don't transcribe the same one again
                transcribed.append(combined_recording)
                
                previous_files = current_files
            continue
        


