import os
import numpy as np
import pretty_midi  


def note_prevalence(midi_data, pitched_inst_only=False, drum_only=False) :  
    
    all_note_on = {}
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
            inst_name = instrument.name if instrument.name != "" else "unknown"             
            id_ = "program_{}_name_{}".format(instrument.program, instrument.name)
            all_note_on[id_] = len(instrument.notes)
    
    for k,v in all_note_on.items():
        all_note_on[k] = v/total_note_on_count 

    return all_note_on 

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
