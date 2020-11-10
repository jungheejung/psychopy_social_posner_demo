#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a practice test for the social posner cueing paradigm
Please change the main_dir to your local directory
"""

from psychopy import core, gui, visual, event
from random import choice
import time
import os
import pandas as pd

__author__ = "Heejung Jung"
__copyright__ = "Copyright (c) 2020 jungheejung"
__version__ = "1.0.1"
__email__ = "heejung.jung@colorado.edu"
__status__ = "Production"

"""
parameters
"""
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

# 7) instruction message
start_msg = 'Please wait. \nThe game will start shortly.'
in_between_run_msg = 'Thank you.\n Please wait for the next game to start'
end_msg = 'This is the end of the experiment. \nPlease wait for instructions from the experimenter'

"""
start experiment
"""
# 1. prompt ____________________________________________________________________
# if this crashes, try installing PyQt5: pip install PyQt5
# but make sure to install specific version, otherwise clashes with other libraries
# https://github.com/CorentinJ/Real-Time-Voice-Cloning/issues/109
# buggy ________________________________________________________________________

#session_info = {'subject_id': 'Type Participant ID', 'RA_Initials': 'Type RA initials'}
#date_Str = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time
#file_prefix = date_Str + ' sub-' + session_info['subject_id'] + '_obsvr_'+session_info['RA_Initials']
#infoDlg = psychopy.gui.DlgFromDict(dictionary = session_info, title = "Spatial Cueing Paradigm", fixed = ['subject_id'])

"""
experiment loop
"""
condition_list = ['practice', 'arrow'] # two conditions = equivalent of block runs
for ind, cond in enumerate(condition_list):

    # step 0. load parameters __________________________________________________
    # 1) load cue - per block
    img_left = os.sep.join([stimuli_dir,cond,"left.png"])
    img_right = os.sep.join([stimuli_dir,cond,"right.png"])
    img_neutral =  os.sep.join([stimuli_dir,cond,"neutral.png"])

    left_gaze = visual.ImageStim(disp, image = img_left, size = (300,300), units="pix")
    right_gaze = visual.ImageStim(disp, image = img_right, size =  (300,300),units="pix")
    neutral_gaze = visual.ImageStim(disp, image =  img_neutral,size =  (300,300), units="pix")
    cue_dict = {'left':left_gaze, 'right':right_gaze, 'neutral':neutral_gaze}

    # 2) load design matrix parameters
    filename = os.sep.join([main_dir, 'design', 'task-practice.csv'])
    cb_parameters = pd.read_csv(filename)

    # step 1. start instruction keys ___________________________________________
    start = visual.TextStim(disp, text=start_msg)
    disp.mouseVisible = False
    start.draw()  # Automatically draw every frame
    disp.flip()

    # step 2. trigger + set clock + dummy scans ________________________________
    # 1) trigger
    event.waitKeys(keyList = 's') # experimenter start key - safe key before fMRI trigger
    event.waitKeys(keyList='5') # fMRI trigger
    # 2) set clock
    kbClock = core.Clock()
    experimentClock = core.Clock()
    experimentClock.reset()
    # 3) wait 6 TRs, dummy scans
    TR = 0.46
    core.wait(TR*6)

    # step 3. create dataframe - will later save
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
    # step 4. fixation ______________________________________________________________
        fixation_cross.draw()
        disp.flip()
        df.loc[index, 'fixation_onset'] = experimentClock.getTime() # save fixation onset time
        trialClock.reset()
        # 4-1. prepare cue in the background
        df.loc[index, 'cue_direction'] = row.cue_direction
        cue_dict[row.cue_direction].draw()
        while trialClock.getTime() < row.fixation_dur: # fixation duration
            continue

    # step 5. cue ___________________________________________________________________
        disp.flip()# cue
        df.loc[index, 'cue_onset'] = experimentClock.getTime()
        # 5-1. prepare cue & target in the background
        trialClock.reset()
        cue_dict[row.cue_direction].draw()
        target.pos = target_positions[row.target_location]
        df.loc[index, 'target_pos'] = row.target_location
        target.draw()
        while trialClock.getTime() < 0.2: # cue presentation
            continue

    # step 6. target ________________________________________________________________
        disp.flip() # target presented
        target_onset = experimentClock.getTime()
        df.loc[index, 'target_onset'] = target_onset
        trialClock.reset()
        kbClock.reset()

    # step 7. get response from participant ____________________________________
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

    # step 8. save run file ____________________________________________________
    # file_savename = os.sep.join([main_dir, 'data', session_info['session_id'], 'practice.csv'])
    file_savename =  os.sep.join([main_dir, 'data', 'fix_prompt', 'practice.csv'])
    df.to_csv(file_savename)

    # step 9. end of run, wait for experimenter instructions ___________________
    message = visual.TextStim(disp, text=in_between_run_msg)
    message.draw()
    disp.flip()
    event.waitKeys(keyList = 'e')

"""
end of experiment
"""
message = visual.TextStim(disp, text=end_msg)
message.draw()
disp.flip()
disp.close()
