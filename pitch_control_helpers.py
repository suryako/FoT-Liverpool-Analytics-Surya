import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage
from tqdm import tqdm
from joblib import Parallel, delayed
import glob
import os
import os.path
import re

sys.path.append('./LaurieOnTracking')
import Metrica_Viz as mviz
import Metrica_IO as mio
import Metrica_Velocities as mvel
import Metrica_PitchControl as mpc

sys.path.append('./lastrow_to_fot/lastrow_to_friendsoftracking')
import lastrow_to_friendsoftracking as lrfot

from pitch_control_helpers import *

def initialise_persistent_play_data(data_attack, data_defence, play, field_dimen=(106.,68.), n_grid_cells_x=50):
    n_grid_cells_y = int(n_grid_cells_x*field_dimen[1]/field_dimen[0])
    xgrid = np.linspace( -field_dimen[0]/2., field_dimen[0]/2., n_grid_cells_x)
    ygrid = np.linspace( -field_dimen[1]/2., field_dimen[1]/2., n_grid_cells_y )
    
    data_attack_play = mvel.calc_player_velocities(data_attack.loc[(play)],smoothing=False)
    data_defence_play = mvel.calc_player_velocities(data_defence.loc[(play)],smoothing=False)
    
    return(data_attack_play, data_defence_play, xgrid, ygrid)


def generate_lvp_pc_time(data_attack_play, data_defence_play, xgrid, ygrid, t=0, frame=None, output_mode='plot'):
    fps = 20
    if not frame: frame = int(fps*t)

    params=mpc.default_model_params(2)

    ball_pos = np.array([data_attack_play.loc[frame].ball_x, data_attack_play.loc[frame].ball_y])
   

    PPCFa = np.zeros( shape = (len(ygrid), len(xgrid)) )
    PPCFd = np.zeros( shape = (len(ygrid), len(xgrid)) )

    attacking_players = mpc.initialise_players(data_attack_play.loc[frame],'attack', params=params)
    defending_players = mpc.initialise_players(data_defence_play.loc[frame],'defense', params=params)

    for i in range( len(ygrid) ):
            for j in range( len(xgrid) ):
                target_position = np.array( [xgrid[j], ygrid[i]] )
                PPCFa[i,j],PPCFd[i,j] = mpc.calculate_pitch_control_at_target(target_position, attacking_players, defending_players, ball_pos, params)
        # check probability sums within convergence
    
    # just return the raw output
    if output_mode=='raw':
        return(PPCFa)
    
    # returning some kind of visuals
    else:
        fig, ax = mviz.plot_pitchcontrol_for_liverpool(data_attack_play, data_defence_play, xgrid, ygrid, frame, PPCFd, annotate=True )

        if output_mode=='plot': 
            return(fig, ax)
        elif output_mode=='vid_artist':
            image = mplfig_to_npimage(fig)
            plt.close()
            return(image)
        else:
            print('Invalid output mode!')
    
def generate_full_lvp_pc(persistent_play_data, fps=20):
    full_play_pc = []
    for frame_num in tqdm(range(persistent_play_data[0].index.max()+1)):
        frame_pc = generate_lvp_pc_time(*(persistent_play_data), frame=frame_num, output_mode='raw') # tuple
        full_play_pc.append(frame_pc)
        
    return(full_play_pc)

def full_lvp_pc_video(persistent_play_data, full_play_pc, fps=20):
    n_frames = persistent_play_data[0].index.max() + fps
    t_length = n_frames/fps
    
    clip = mpy.VideoClip(lambda x: mviz.plot_pitchcontrol_for_liverpool(*(persistent_play_data), int(fps*x), full_play_pc[int(fps*x)], output_mode='vid_artist'), duration=t_length-1).set_fps(fps)
    return clip
