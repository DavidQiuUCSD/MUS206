# Imports
#  -*- coding: utf-8 -*-
import numpy as np
import pretty_midi
import librosa
import os
import json
import csv
# Local path constants
DATA_PATH = r'C:\Users\zhiho\tacotron\Lakh'
# Path to the file match_scores.json distributed with the LMD
#SCORE_FILE = os.path.join(DATA_PATH, 'match_scores.json')
SCORE_FILE = os.path.join(r'C:\Users\zhiho\tacotron\Lakh\match_scores.json')

OUTPUT_WAV = r'C:\Users\zhiho\tacotron\Lakh\wavs'

OUTPUT_CSV = r'C:\Users\zhiho\tacotron\Lakh\metadata.csv'


# Utility functions for retrieving paths
def msd_id_to_dirs(msd_id):
    """Given an MSD ID, generate the path prefix.
    E.g. TRABCD12345678 -> A/B/C/TRABCD12345678""" 
    #print os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)
    return os.path.join(msd_id[2], msd_id[3], msd_id[4], msd_id)

def msd_id_to_mp3(msd_id):
    """Given an MSD ID, return the path to the corresponding mp3"""
    #print os.path.join(DATA_PATH, 'lmd_matched_mp3',
    #                    msd_id_to_dirs(msd_id) + '.mp3')
    return os.path.join(DATA_PATH, 'lmd_matched_mp3',
                        msd_id_to_dirs(msd_id) + '.mp3')

def get_midi_path(msd_id, midi_md5, kind):
    """Given an MSD ID and MIDI MD5, return path to a MIDI file.
    kind should be one of 'matched' or 'aligned'. """
    return os.path.join(DATA_PATH, 'lmd_{}'.format(kind),
                        msd_id_to_dirs(msd_id), midi_md5 + '.mid')

def extract_avg_in_col(arr):
    max  = 0
    result = 0
    for i in range(len(arr)):
        if arr[i] > max:
            max = arr[i]
            result = i * 6 + (int)(max*6/1000) + 33
    return chr(result)

    #arr = arr.T
    #for r in arr:
    #nonzeros = [x for x in arr if x > 0.0]
    #avg = np.mean(nonzeros) if len(nonzeros)>0 else 0.0
    #result.append(avg)
    #return avg

with open(SCORE_FILE) as f:
    scores = json.load(f)
# (midi,audio) pairs
result_pairs = []
index = 0
while len(result_pairs) < 500 and scores:
    index+=1
    print ("running....", index)
    # Grab an MSD ID and its dictionary of matches
    msd_id, matches = scores.popitem()
#    print (matches)
    # Grab a MIDI from the matches
    midi_md5, score = matches.popitem()
    # Construct the path to the aligned MIDI
    aligned_midi_path = get_midi_path(msd_id, midi_md5, 'aligned')
    # Load/parse the MIDI file with pretty_midi
    pm = pretty_midi.PrettyMIDI(aligned_midi_path)
   
    # MIDI files in LMD-aligned are aligned to 7digital preview clips from the MSD
    # Let's listen to this aligned MIDI along with its preview clip
    # Load in the audio data
    #librosa.core.load(path, sr=22050, mono=True, offset=0.0, duration=None)
    #maybe we can make more use of offset and duration when trying to divide music pieces
    audio, fs = librosa.load(msd_id_to_mp3(msd_id), sr = 20000)
    midi_matrix = pm.get_chroma(fs)
    col = midi_matrix.shape[1]
    midi_matrix_30 = midi_matrix[:,:col-1]
    sample = np.linspace(0,col-1,(col-1)/420,endpoint = False, dtype = np.int32)
    compressed_midi = midi_matrix_30[:,sample]
    
    pieceCount = 10
    cutpointAudio = (int)(audio.shape[0]/pieceCount)
    cutpointMidi = (int)(compressed_midi.shape[1]/pieceCount)
    for i in range(pieceCount):
        id = 'l-%05d-%d' % (index , i)
        # save compressed midi matrix to a file
        mat = compressed_midi[:, (cutpointMidi*i) : (cutpointMidi*(i+1))]
        array_char = np.apply_along_axis(extract_avg_in_col, 0, mat)
        #array_char = [chr(x) for x in array_int]
        with open(OUTPUT_CSV, 'a', newline = '') as csv_file:
            #csv_file.write(id + ' | ' + array_char.tostring())
            datawriter = csv.writer(csv_file, delimiter = '|')
            datawriter.writerow([id, ''.join(array_char.tolist())])
        #save audio to a file
        librosa.output.write_wav(os.path.join(OUTPUT_WAV, id + '.wav'), audio[cutpointAudio*i:cutpointAudio*(i+1)], fs)


        #result_pairs.append((mat_avg, audio[cutpoint*i:cutpoint*(i+1)]))
        print("audio",cutpointAudio*i)
        print("midi", cutpointMidi*i)
        #print ("# of nonzero values : ",np.count_nonzero(mat))
        #print("first col : ",mat[:,0])
        #print("max : ",np.amax(mat,axis = 0)[0]," min : ",np.amin(mat,axis = 0)[0])
        #print("the first note's avg pitch : ", mat_avg[0])


