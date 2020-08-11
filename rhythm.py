import os
import pretty_midi
import numpy as np
from .utils import make_id 

def autocorrelate(sequence):
    pass

def beat_histogram():
    pass

def instrument_note_density_per_second(midi_inst):
    
    midi_inst.is_drum = False 
    piano_roll = midi_inst.get_piano_roll()
    piano_roll[piano_roll > 0] = 1 
    
    density = np.sum(piano_roll) / piano_roll.shape[1] * 100 
    return density 


def note_density_per_second(midi_data):
    '''
    Computes the note density per second for each instrument and for all tracks 
    Args : 
        midi_data: pretty_midi midi object
    Returns : 
        output : dictionary with each instrument ('program_x_name_y' or 'total'  as key) and value is note density per second (float)  
    '''

    output = {} 

    total_piano_roll = np.zeros((128 * len(midi_data.instruments), midi_data.get_piano_roll().shape[1])) 
    for i, midi_inst in enumerate(midi_data.instruments): 
        if midi_inst.is_drum : 
            midi_inst.is_drum = False
        piano_roll = midi_inst.get_piano_roll()
        piano_roll[piano_roll > 0] = 1 
        
        density = np.sum(piano_roll) / piano_roll.shape[1] * 100 
        
        total_piano_roll[128 * i : (i+1) * 128,:]=piano_roll 
        id_ = make_id(midi_inst)
        output[id_] = density

    
    total_density = np.sum(total_piano_roll) / total_piano_roll.shape[1] *100
    output['total'] = total_density 
    return output 


def note_duration_mean_and_std(midi_data):
    ''' 
    Returns mean and std of note duration per instrument. 
    Computed over all the note on events. 
    
    Args : 
        midi_data : pretty_midi midi object 
    Return:
        output : dictionary with each instrument ('program_x_name_y' as key) and value is a tuple of (mean, std) 
    ''' 
    output = {}
    for i, midi_inst in enumerate(midi_data.instruments):
        avg_duration = [] 
        for note in midi_inst.notes:
            avg_duration.append(note.get_duration())

        name = midi_inst.name if midi_inst.name != "" else "unknown"
        id_ = make_id(midi_inst)
        output[id_] = (np.mean(avg_duration), np.std(avg_duration))
    
    return output 






if __name__ =='__main__' :
    midi_data = pretty_midi.PrettyMIDI('./data/302_Somari_09_10Boss.mid')
    # density = note_density_per_second(midi_data)
    note_duration = note_duration_mean_and_std(midi_data)
    print (note_duration) 


    
