from Autoprotocol import *
from Inventory import *
from InventoryFactory import *
from LabPlanner import *
from LabPacketFactory import *
from ExperimentFactory import *
from Serializer import *
from Parser import *

pcr1 = PCR('PCR', 'pcrpdt', 'ca1067F', 'ca1067R', 'pSB1AK3-b0015', 1000)
dig1 = Digest('Digest', 'pcrdig', 'pcrpdt', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
dig2 = Digest('Digest', 'vectdig', 'pSB1A2-I13521', [Reagent.EcoRI, Reagent.SpeI], 'A', 1000)
lig = Ligate('Ligate', 'pSB1A2-Bca9128', ['pcrdig', 'vectdig'])
trans = Transform('Transform', 'finalpdt', 'pSB1A2-Bca9128', 'Mach1', ['Amp'], 37)
seqs = {'pSB1A2-I13521': 'randomsequencehere'}

pcr2 = PCR('PCR', 'pcrOutput', 'oligoF', 'oligoR', 'template', 500)

cflist = [ConstructionFile([pcr1, dig1, dig2, lig, trans], seqs), ConstructionFile([pcr2], None)]
ser = Serializer()
par = Parser()

EF = ExperimentFactory()
exp = EF.run('Test', 'TestID', cflist, None)
ser.serializeLabPacket(exp.labPacket, 'out-labpacket')
ser.serializeInventory(exp.inventory, 'out-inventory')

inv = par.parseInventory('out-inventory')
box = par.parseBoxRowForm('out-inventory/0-Box.txt')
ser.serializeBoxRowForm(box, 'out-inventory/test.txt')