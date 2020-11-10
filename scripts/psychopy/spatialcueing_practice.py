#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a practice test for the social posner cueing paradigm
"""

__author__ = "Heejung Jung"
__version__ = "1.0.1"
__email__ = "heejung.jung@colorado.edu"
__status__ = "Production"

from psychopy import core, gui, visual, event
from random import choice
import time
import os
import pandas as pd

# parameters ___________________________________________________________________

# 1) directory
main_dir = "/Users/h/Dropbox/projects_dropbox/psychopy_social_posner_demo"
stimuli_dir = main_dir + os.sep + "stimuli"

# 2) color
GREY = [128, 128, 128]
BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
YELLOW = [255, 255, 0]
GREEN = [0, 255, 0]
RED = [255, 0, 0] #[1,-1,-1]
cue_color = YELLOW
background_color = GREY

# 3) window
disp = visual.Window(pos=(0, 0), color=background_color, colorSpace="rgb255", units="norm", fullscr=True)

# 4) fixation
fixation_cross = visual.TextStim(win = disp, text = '+', color = [-1,-1,-1], height = 0.3)

# 5) target
target = visual.Circle(win = disp, units = 'pix', radius = 15, edges=128, lineColor=[-1,-1,-1], lineColorSpace='rgb', fillColor=[-1,-1,-1], fillColorSpace='rgb')
target_positions = {'left': (int(disp.size[0] * -0.2), 0), 'right':( int(disp.size[0] * 0.2), 0)}

# 6) keyboard map
key_map = {'1': 'left', '2': 'right'}


# start experiment ___________________________________________________________________
# 1. prompt ___________________________________________________________________
# if this crashes, try installing PyQt5: pip install PyQt5
# but make sure to install specific version, otherwise clashes with other libraries
#https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues/109
#session_info = {'subject_id': 'Type Participant ID', 'RA_Initials': 'Type RA initials'}
#date_Str = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time
#file_prefix = date_Str + ' sub-' + session_info['subject_id'] + '_obsvr_'+session_info['RA_Initials']
#infoDlg = psychopy.gui.DlgFromDict(dictionary = session_info, title = "Spatial Cueing Paradigm", fixed = ['subject_id'])

# ______________________________________________________________________________
condition_list = ['practice', 'arrow'] # two conditions = equivalent of block runs
for ind, cond in enumerate(condition_list):
    # condition specific parameters ____________________________________________________
    # 1) cue
    img_left = os.sep.join([stimuli_dir,cond,"left.png"])
    img_right = os.sep.join([stimuli_dir,cond,"right.png"])
    img_neutral =  os.sep.join([stimuli_dir,cond,"neutral.png"])

    left_gaze = visual.ImageStim(disp, image = img_left, size = (300,300), units="pix")
    right_gaze = visual.ImageStim(disp, image = img_right, size =  (300,300),units="pix")
    neutral_gaze = visual.ImageStim(disp, image =  img_neutral,size =  (300,300), units="pix")
    cue_dict = {'left':left_gaze, 'right':right_gaze, 'neutral':neutral_gaze}

    # 2) load design parameters
    filename = os.sep.join([main_dir, 'design', 'task-pracetice.csv'])
    cb_parameters = pd.read_csv(filename)
    # ______________________________________________________________________________

    # start instruction keys
    start = visual.TextStim(disp, text='Please wait. \nThe game will start shortly.')
    disp.mouseVisible = False
    start.draw()  # Automatically draw every frame
    disp.flip()
    event.waitKeys(keyList = 's') # experimenter start key - safe key before fMRI trigger
    event.waitKeys(keyList='5') # fMRI trigger

    # 3. set clock _________________________________________________________________
    trialClock = core.Clock()
    kbClock = core.Clock()
    experimentClock = core.Clock()
    experimentClock.reset()

    # wait 6 TR, dummy scans
    TR = 0.46
    core.wait(TR*6)
    
    # create dataframe
    df = pd.DataFrame(columns = ['condition', 'block_order', 'block_number', 'cb_ver', 
    'fixation_onset', 'cue_direction', 'cue_onset','target_pos', 'target_onset', 
    'raw_key_response', 'key_rt', 'keypress', 'key_conversion'])
    df['condition'] = cb_parameters['cue_type']
    df['block_order'] = ind
    df['block_number'] = 1
    df['trial_type'] = cb_parameters['condition_type']
    df['cb_ver'] = cb_parameters['cB_version']
    
    # loop through design parameters _______________________________________________
    for index, row in cb_parameters.iterrows():

        # 4. fixation ______________________________________________________________
        fixation_cross.draw()
        disp.flip()
        df.loc[index, 'fixation_onset'] = experimentClock.getTime() # save fixation onset time
        trialClock.reset()
        # 4-1. prepare cue in the background
        df.loc[index, 'cue_direction'] = row.cue_direction
        cue_dict[row.cue_direction].draw()
        while trialClock.getTime() < row.fixation_dur: # fixation duration
            continue
            
        # 5. cue ___________________________________________________________________
        disp.flip()# cue
        # cue_onset = experimentClock.getTime()
        df.loc[index, 'cue_onset'] = experimentClock.getTime()
        # 5-1. prepare cue & target in the background
        trialClock.reset()
        cue_dict[row.cue_direction].draw()
        target.pos = target_positions[row.target_location]
        df.loc[index, 'target_pos'] = row.target_location
        target.draw()
        while trialClock.getTime() < 0.2: # cue presentation
            continue
            
        # 6. target ________________________________________________________________
        disp.flip() # target presented
        target_onset = experimentClock.getTime()
        df.loc[index, 'target_onset'] = target_onset
        trialClock.reset()
        kbClock.reset()
        
        # 7. get response from participant __________________________________________
        while trialClock.getTime() <= 2.5: #and not responded:
            keys = event.getKeys(keyList = ['1', '2'])
            if len(keys) > 0:
                print(keys)
                df.loc[index, 'raw_key_response'] = keys[0]
                rt = kbClock.getTime()
                keypresstime = experimentClock.getTime()
                df.loc[index, 'keypress'] = keypresstime
                df.loc[index, 'key_rt'] = rt
                df.loc[index, 'key_conversion'] = key_map[keys[0]]
        kbClock.reset()
        
    # 8. save run file __________________________________________
    # file_savename = os.sep.join([main_dir, 'data', session_info['session_id'], 'practice.csv'])
    file_savename =  os.sep.join([main_dir, 'data', 'fix_prompt', 'practice.csv'])
    df.to_csv(file_savename)

     # 9. End of Run, Wait for experimenter instructions__________________________________________
    message = visual.TextStim(disp, text='Thank you.\n Please wait for the next game to start')
    message.draw()  
    disp.flip()
    event.waitKeys(keyList = 'e')

# End of experiment __________________________________________
message = visual.TextStim(disp, text='This is the end of session 1. \nPlease wait for instructions from the experimenter')
message.draw()  # Automatically draw every frame
disp.flip()
disp.close()
