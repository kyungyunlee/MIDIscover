import os
import numpy as np
import pretty_midi  
from .utils import make_id 


def note_prevalence(midi_data, pitched_inst_only=False, drum_only=False) :  
    '''
    Computes the fraction of note on events of each instrument over the entire note on events.
    (# of note on events of instrument X) / (# of note on events for all instruments)
    Args : 
        midi_data : pretty_midi midi object
        pitched_inst_only : whether to compute for only non-drum instruments (for computing note prevalence for pitched instruments) 
        drum_only : whether to compute for only drum instruments (for non-pitched instruments) 
    Return : 
        out : dictionary with ('program_X_inst_Y' as key) and fraction as value (float) 
    '''
    
    out = {}
    total_note_on_count = 0 
    for instrument in midi_data.instruments : 
        if pitched_inst_only and instrument.is_drum : 
            total_note_on_count += len(instrument.notes)
            continue
        elif drum_only and not instrument.is_drum : 
            total_note_on_count += len(instrument.notes)
            continue
        else :
            total_note_on_count += len(instrument.notes)
            id_ = make_id(instrument)
            out[id_] = len(instrument.notes)
    
    for k,v in out.items():
        out[k] = v/total_note_on_count 

    return out 

def note_prevalence_variance(midi_data, pitched_inst_only=False, drum_only=False) : 
    all_note_on = note_prevalence(midi_data, pitched_inst_only, drum_only)
    note_on_array = [v for k,v in all_note_on.items()]
    return np.std(note_on_array)
    

        

if __name__ == '__main__':
    midi_data = pretty_midi.PrettyMIDI('./data/302_Somari_09_10Boss.mid') 
    note_on = note_prevalence(midi_data, pitched_inst_only=False)
    print (note_on)
    std = note_prevalence_variance(midi_data) 
    print (std) 
