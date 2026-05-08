from Inventory import *
import pickle

class Parser:
    '''
    This class contains all functions for parsing files.
    '''
    def parseBoxRowForm(self, inpath):
        '''
        Parameters:
            inpath: the path of a previously serialized box to be parsed
        Returns:
            a Box object 
        '''
        samplesArray = [[None for _ in range(10)] for _ in range(10)]
        with open(inpath, 'r') as f:
            lines = f.readlines()
            name = lines[0].split()[1]
            description = lines[1].split()[1]
            location = lines[1].split()[1]
            for i in range(5, len(lines)):
                lineArr = lines[i].split()
                sidelabel = lineArr[2]
                concentration = lineArr[3]
                culture = lineArr[5]
                clone = lineArr[6]
                if sidelabel == 'None':
                    sidelabel = None
                if concentration != 'None':
                    concentration = Concentration(lineArr[3])
                else:
                    concentration = None
                if culture != 'None':
                    culture = Culture(lineArr[5])
                else:
                    culture = None
                if clone == 'None':
                    clone = None
                sample = Sample(lineArr[1], sidelabel, concentration, lineArr[4], culture, clone)
                samplesArray[ord(lineArr[0][0]) - 65][int(lineArr[0][1])] = sample
        
        return Box(name, description, location, samplesArray)


    def parseInventory(self, indir):
        '''
        Parameters:
            indir: the directory of a previously serialized Inventory object to be parsed
        Returns:
            an Inventory object 
        '''
        boxes = []
        with open(f'{indir}/construct_to_locations', 'rb') as f:
            construct_to_locations = pickle.load(f)
        
        with open(f'{indir}/location_to_concentration', 'rb') as f:
            loc_to_conc = pickle.load(f)
        
        with open(f'{indir}/location_to_clone', 'rb') as f:
            loc_to_clone = pickle.load(f)
        
        with open(f'{indir}/location_to_culture', 'rb') as f:
            loc_to_culture = pickle.load(f)
    
        return Inventory(boxes, construct_to_locations, loc_to_conc, loc_to_clone, loc_to_culture)
    