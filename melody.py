import os
import pretty_midi
import numpy as np


def melodic_interval_histogram(midi_inst, normalized=True):
    '''
    Histogram of melodic intervals 
    Array of 73 bins where each bin corresponds to interval amounts in semitones. It ranges from -36 to 36 semitones in order. 
    Args : 
        midi_inst : pretty_midi instrument object
        normalized : bool 
    Return : 
        intervals : numpy array of shape=((73,))
    '''
    intervals = np.zeros((73,)) # 3 octaves down and up  
    midi_notes = midi_inst.notes
    for i in range(1, len(midi_notes)): 
        prev_note = midi_notes[i-1]
        curr_note = midi_notes[i]
        time_diff = curr_note.start - prev_note.end 
        if time_diff > 1:
            continue 
        else : 
            pitch_diff = curr_note.pitch - prev_note.pitch   
            if pitch_diff == 0 : 
                intervals[36] += 1 
            else : 
                interval_idx = pitch_diff + 36
                intervals[interval_idx] +=1 

    
    if normalized : 
        intervals /= np.sum(intervals)

    return intervals


def average_melodic_interval(midi_inst):
    intervals = melodic_interval_histogram(midi_inst, normalized=False)
    sum_intervals = 0 
    for i, n_itv in enumerate(intervals) : 
        itv = i - 36 
        sum_intervals += abs(itv) * n_itv

    return sum_intervals / np.sum(intervals)

        
def most_common_melodic_interval(midi_inst):
    intervals = melodic_interval_histogram(midi_inst, normalized=False)
    top_itv = np.argwhere(intervals == np.amax(intervals))
    top_itv = np.array([x[0] for x in top_itv]) 
    top_itv -= 36
    return top_itv

def melodic_interval_fractions(midi_inst, interval_amt):
    '''
    interval_amt can be one of ['semitone', 'thirds', 'fifths', 'tritones', 'octaves'] 
    semitone : 1 semitone
    thirds : minor and melodic thirds (3 and 4 semitones) 
    fifths : perfect fifths (7 semitones)
    tritones : 1 tritone (6 semitones)
    octaves : 1 or more octaves (multiple of 12 semitones)
    '''
    if interval_amt not in ['semitones', 'thirds', 'fifths', 'tritones', 'octaves']:
        raise ValueError("'interval_amt' cannot be identified. Choose from ['semitones', 'thirds', 'fifths', 'tritones', 'octaves']") 

    intervals = melodic_interval_histogram(midi_inst, normalized=False)

    if interval_amt == 'semitones' : 
        n = intervals[35] + intervals[37]
    elif interval_amt == 'thirds' : 
        n = intervals[32] + intervals[39] + intervals[33] + intervals[38]
    elif interval_amt == 'fifths' : 
        n = intervals[29] + intervals[42] 
    elif interval_amt == 'tritones':
        n = intervals[30] + intervals[41]
    else:
        n = intervals[36 - 12] + intervals[36 + 12] + intervals[36 - 24] + intervals [36 + 24] + intervals[0] + intervals[-1] 
    return n / np.sum(intervals)


def direction_of_melody(midi_inst):
    '''
    To find out whether the melody is directed down or up. 
    Returns the fraction of counts of both down and up intervals. 
    Larger number of the two tells us that the given melody has more tendency to go up or down. 
    
    Args :
        midi_inst : pretty_midi instrument object 
    Return :
        (fraction of down, fraction of up) 
    '''
    intervals = melodic_interval_histogram(midi_inst, normalized=False)
    down = np.sum(intervals[:36])
    up = np.sum(intervals[37:]) 
    return down / np.sum(intervals), up / np.sum(intervals)




if __name__ =='__main__' :
    midi_data = pretty_midi.PrettyMIDI('./data/302_Somari_09_10Boss.mid')
    # a = melodic_interval_histogram(midi_data.instruments[1])
    # a = average_melodic_interval(midi_data.instruments[1])
    # a = most_common_melodict_interval(midi_data.instruments[1])
    # a = melodic_interval_fractions(midi_data.instruments[1], 'octaves')
    a = direction_of_melody(midi_data.instruments[1])


    print (a)
