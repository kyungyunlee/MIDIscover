

def make_id(midi_instrument):
    '''
    midi instrument representation with program number of instrument name 
    args : 
        midi_instrument : pretty_midi instrument object 
    return : 
        id_ : 'program_X_name_Y' where X = instrument's program number, Y = instrument name 
    ''' 
    name = midi_instrument.name if midi_instrument.name != "" else "unknown"
    id_ = "program_{}_name_{}".format(midi_instrument.program, name)
    return id_ 


