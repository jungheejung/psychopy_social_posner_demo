from psychopy import core, visual, gui,event
from psychopy.hardware import keyboard
from random import choice
import time
import os
import pandas as pd

# parameters ___________________________________________________________________
#logger = logging.getLogger("tendo.singleton")
#logger.addHandler(logging.StreamHandler())

# 1) directory
main_dir = "/Users/h/Dropbox/Projects/SI.01_git"
stimuli_dir = main_dir + os.sep + "stimuli"

# 2) color
GREY = [128, 128, 128]
BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
YELLOW = [255, 255, 0]
GREEN = [0, 255, 0]
RED = [255, 0, 0]
cue_color = YELLOW
background_color = GREY
# 3) window
disp = visual.Window(pos=(0, 0), color=background_color, colorSpace="rgb255", fullscr=False, units="norm")
# 4) fixation
fixation_cross = visual.TextStim(win = disp, text = '+', color = 'white', height = 0.3)
# 6) target
target = visual.Circle(win = disp, units = 'pix', radius = 12, edges=128, lineColor=[1.0,-1,-1], lineColorSpace='rgb', fillColor=[1.0,-1,-1], fillColorSpace='rgb')
target_positions = {'left': (int(disp.size[0] * -0.25), 0), 'right':( int(disp.size[0] * 0.25), 0)}
# 7) keyboard
kb = keyboard.Keyboard()
event.globalKeys.add(key = 'escape', func = core.quit, modifiers = ['ctrl'])
# 8) keyboard mapp
key_map = {'f': 'left', 'j': 'right'}


# start experiment
# 1. prompt ___________________________________________________________________
session_info = {'Observer': 'Type observer ID', 'Participant': 'Type participant ID'}
date_Str = time.strftime("%b_%d_%H%M", time.localtime())  # add the current time
file_prefix = date_Str + ' pcpnt_' + session_info['Participant'] + '_obsvr_'+session_info['Observer']
dlg_box = gui.DlgFromDict(session_info, title="Spatial Cueing Paradigm", fixed=["date"])

# ______________________________________________________________________________

# FOR LOOP START
condition_list = ['arrow','parent_CJ'] #, 'parent_CJ', 'parent_JW', 'interest_CJ', 'interest_JW']
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
    filename = os.sep.join([main_dir, 'design', 'task-' + cond + '_counterbalance_ver-01_block-01.csv'])
    cb_parameters = pd.read_csv(filename)
    # ______________________________________________________________________________



    # get 
    event.waitKeys(keyList='5')
    # 3. set clock _________________________________________________________________
    trialClock = core.Clock()
    experimentClock = core.Clock()
    experimentClock.reset()

    # create dataframe
    df = pd.DataFrame(columns = ['condition', 'block_order', 'block_number', 'cb_ver', 'fixation_onset', 'cue_direction', 'cue_onset','target_pos', 'target_onset', 'raw_key_response', 'key_rt', 'key_conversion'])
    df['condition'] = cb_parameters['cue_type']
    df['block_order'] = ind
    df['block_number'] = ind
    df['trial_type'] = cb_parameters['condition_type']
    df['cb_ver'] = cb_parameters['cB_version']
    # loop through design parameters _______________________________________________
    for index, row in cb_parameters.iterrows():
        
        # 4. fixation ______________________________________________________________
        fixation_cross.draw()
        disp.flip()
        # fixation_onset = experimentClock.getTime()
        df.loc[index, 'fixation_onset'] = experimentClock.getTime()
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
        # target_onset = experimentClock.getTime()
        df.loc[index, 'target_onset'] = experimentClock.getTime()
        trialClock.reset()
        kb.clock.reset()
        # 7. get response from participant __________________________________________
        responded = False
        while trialClock.getTime() <= 2.5: #and not responded:
            ptbKey = kb.getKeys(keyList = ['f', 'j'], waitRelease = False, clear = True)
            if ptbKey:
                print(ptbKey[0].name, ptbKey[0].rt)
                df.loc[index, 'raw_key_response'] = ptbKey[0].name
                df.loc[index, 'key_rt'] = ptbKey[0].rt
                df.loc[index, 'key_conversion'] = key_map[ptbKey[0].name]
    file_savename = os.sep.join([main_dir, 'data', 'sub-01', 'sub-01_task-' + cond + '_beh.csv'])
    df.to_csv(file_savename)
    
    # thank you screen
    message = visual.TextStim(disp, text='Thank you. Please wait for the next game to start')
    message.autoDraw = True  # Automatically draw every frame
    disp.flip()
    

# for index, row in cb_parameters.iterrows():
#     keyRT, keyname = trial_sequence(row)
#     cb_parameters.at[index,'keyRT'] = keyRT
#     cb_parameters.at[index,'keyname'] = keyname
# save_file = os.path.join(save_dir + "\\" + file_prefix + ".csv")
# ---------------- >8 ----------------------------------------------------------
# Escape keys
# 1) add a global event key
#from psychopy.preference import prefs
#prefs.general['shutdownKey'] = 'escape'
#
## 2) look for esc
#continuing = True
#if pygKey == 'escape':
#    continuing = False
## 3) add global keys
# win = Window()
# #win_width, win_height = 1920, 1080
# win_width, win_height = win.size[0], win.size[1]
# win_dimension = (win_width, win_height)



#left_gaze.size = left_gaze.size * 0.8
#right_gaze.size = right_gaze.size * 0.8
#neutral_gaze.size = neutral_gaze.size * 0.8

#
#
#
#
# def trial_sequence(row):
#     ## 1. Fixation
#     fixation_cross.draw()
#     disp.flip()
#     trialClock.reset()
#
#     ## 2. draw cue
#     # read pandas row
#     # depending on what the row is, read in left/right/neutral gaze
#     if row.cue_direction == 'left':
#         left_gaze.draw()
#     elif row.cue_direction == 'right':
#         right_gaze.draw()
#     elif row.cue_direction == 'neutral':
#         neutral_gaze.draw()
#     while trialClock.getTime() < 2: # fixation duration
#         continue
#
#     disp.flip()# cue
#     trialClock.reset()
#
#     ## 3. draw target
#     trialClock.reset()
#     if row.target_location == 'left':
#         left_target.draw()
#     elif row.target_location == 'right':
#         right_target.draw()
#     while trialClock.getTime() < 0.5: # cue duration
#         continue
#
#     ## 4. flip target target
#     disp.flip()
#     trialClock.reset()
#     kb.clock.reset()
#     responded = False
#     while trialClock.getTime() <= 4 and not responded: # target duration and wait for self-paced response
#
#         ptbKey = kb.getKeys(keyList = ['f', 'j'], waitRelease = False, clear = True)
#         for key in ptbKey:
#             print(key.name, key.rt)
#             keypress = key.rt
#             keyname = key.name
# #        if ptbKey:
# #            responded = True
# #            print(ptbKey.rt)
# #            print(ptbKey.name)
#             # check if response is correct
#         continue
#
#     return keypress, keyname
#
#
# def convertRGB(RGB):
#     """function to convert RGB guns from 255-range values to normalised values for PsychoPy"""
#     normalised_color = []
#     for gun in RGB:
#         normV = ((1/127.5)*gun)-1
#         normalised_color.append(normV)
#
#     return normalised_color

# synchronization pulse / interlaced / progressive / lcd: memory
# ------------------------------------------------------- >8 -------------------
