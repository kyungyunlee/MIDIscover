import os
import pretty_midi
import numpy as np


def pitch_histogram(midi_inst, normalized=True):
    '''
    128 bin array (1 for each pitch) where the magnitude represents the number of times the note on appeared for corresponding pitch 
    '''
    histogram = np.zeros ((128,)) 
    for note in midi_inst.notes : 
        histogram[note.pitch - 1] +=1 
    
    if normalized : 
        histogram /= np.sum(histogram)
    return histogram


def pitch_class_histogram(midi_inst, normalized=True):
    '''
    12 bin array (1 for each pitch class) where the magnitude represents the number of times the note on appeared for corresponding pitch class. 
    '''
    histogram = np.zeros((12,))
    for note in midi_inst.notes : 
        pitch_class = (note.pitch -1)%12 
        histogram[pitch_class] += 1 

    if normalized : 
        histogram /= np.sum(histogram)
    return histogram


def most_common_pitch(midi_inst, top_n=1):
    '''
    Find the most commonly occuring pitch 
    Args :
        midi_inst : pretty_midi instrument object
    Return : 
        pitches : numpy array of most common pitches 
    '''
    pitch_hist = pitch_histogram(midi_inst)
    # pitches = np.argwhere(pitch_hist == np.amax(pitch_hist))
    # pitches = [i[0]+1 for i in pitches]
    # return pitches
    sorted_idx = np.argsort(pitch_hist)[::-1]
    sorted_value = pitch_hist[sorted_idx]
    top_list = list(sorted_idx[:top_n])
    last_val = sorted_value[top_n-1] 
    # print (sorted_idx)
    # print (sorted_value)
    # print (top_list)
    # print (last_val)
    for i, (idx, val) in enumerate(zip(sorted_idx, sorted_value)):
        if i < top_n : 
            continue 
        if idx != top_list[-1] and val == last_val :
            top_list.append(idx) 
    top_list = np.array(top_list)
    top_list += 1 
    return top_list 



def most_common_pitch_class(midi_inst, top_n=1): 
    '''
    Find the most commonly occuring pitch classes 
    Args :
        midi_inst : pretty_midi instrument object
    Return : 
        pitches : numpy array of most common pitch classes
    '''
    pitch_hist = pitch_class_histogram(midi_inst)
    # pitches = np.argwhere(pitch_hist == np.amax(pitch_hist))
    # pitches = [i[0] + 1 for i in pitches]
    sorted_idx = np.argsort(pitch_hist)[::-1]
    sorted_value = pitch_hist[sorted_idx]
    top_list = list(sorted_idx[:top_n])
    last_val = sorted_value[top_n-1] 
    for i, (idx, val) in enumerate(zip(sorted_idx, sorted_value)):
        if i < top_n : 
            continue
        if idx != top_list[-1] and val == last_val :
            top_list.append(idx) 
    top_list = np.array(top_list)
    top_list += 1 
    return top_list 


def relative_strength_of_top_pitches(midi_inst):
    pass

def relative_strength_of_top_pitch_classes(midi_inst):
    pass 

def interval_between_strongest_pitches():
    pass

def interval_between_strongest_pitch_classes():
    pass 

def number_of_common_pitches(midi_inst):
    '''
    Number of pitch classes that account for 10% of all notes 
    '''
    hist = pitch_histogram(midi_inst, normalized=False)
    top_n = most_common_pitch(midi_inst, top_n=128)
    sorted_hist = hist[top_n-1]
    total_number_of_notes = np.sum(sorted_hist)
    ten_percent = total_number_of_notes * 0.1 
    
    common_pitches = []
    prev_val = -1 
    for i, (pitch, val) in enumerate(zip(top_n, sorted_hist)):
        if val <= ten_percent : 
            common_pitches.append(pitch)
            prev_val = val 
            ten_percent -= val 
        else :
            if i == 0 :
                common_pitches.append(pitch)
                prev_val = val 
                ten_percent -= val 
            else :
                if prev_val == val : 
                    common_pitches.append(pitch)
                else : 
                    break

    return common_pitches  
    

def pitch_variety(midi_inst):
    '''
    Number of pitches used at least once.
    ''' 
    hist = pitch_histogram(midi_inst)
    return np.count_nonzero(hist)


def pitch_class_variety(midi_inst):
    '''
    Number of pitch classes used at least once. 
    '''
    hist = pitch_class_histogram(midi_inst)
    return np.count_nonzero(hist)


def pitch_range(midi_inst):
    '''
    Range of lowest to higest notes played 
    '''
    hist = pitch_histogram(midi_inst)

    valid_pitches = np.where(hist > 0)[0]

    return valid_pitches[-1] - valid_pitches[0]





if __name__ =='__main__' :
    midi_data = pretty_midi.PrettyMIDI('./data/302_Somari_09_10Boss.mid')
    #  a = most_common_pitch(midi_data.instruments[1])
    # a = pitch_class_variety(midi_data.instruments[1])
    # a = number_of_common_pitches(midi_data.instruments[1])
    a = pitch_range(midi_data.instruments[1])
    print (a) 
