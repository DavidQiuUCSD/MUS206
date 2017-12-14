# MUS206

This repository contains python files that we have written ourselves outside of the original files used in Tacotron found in https://github.com/keithito/tacotron. 

Below is a description of each file. 

# lakh.py

This python file takes in wav files and computes the linear-scale and mel-scale spectrograms, which will then be fed into the blackbox Tacotron model. This file should be added to the dataset folder in the original tacotron.

# preprocess.py

This python file should replace the original preprocess.py in the tacotron folder. We have added some auxillary functions so that the model will properly preprocess the new dataset.

# symbols.py

This python file should replace the original symbols.py file in the text folder. We have edited it so that it contains the proper 72 symbols that we have used in our encoding.

# tranScript.py

This is our encoding script which will properly sort and group each audio and MIDI files together; properly down-sample and encode the MIDI file into the encoded semantic sentence as referenced in our paper and presentation. This script should be run before properly starting Tacotron. 
