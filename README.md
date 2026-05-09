# BioEng134 Final Project - Master Mix Calculator
**Rachel Sang**

## Project Overview

This project builds off of a previous BioEng140L final project that created a LabPlanner codebase, which automated the planning and steps of biological experiments. The preivous developers, in their README.md mentioned the lack of a master mix calculator as a limitation. Creating master mixes for experiments proves advantages in experiments, allowing for more consistent concentrations of reagents across all samples in a simple experiment, reducing plastic pipette tip waste, and reducing the risk of contamination. My individual contribution focuses on implementing a master mix calculator into the pre-existing LabPlanner codebase that calculates scaled reagent volumes for multiple common lab protocols, then integrades these new volumes into the final LabPacket.

---

## Gap in Previous Codebase

In the previous BioEng140L LabPlanner codebase, 'LabPacketFactory.py' hardcoded reagent volumes per sample for each supported experiment type. Therefore, there was no way to scale up the recipes for experiments with varying number of samples, and the 10% buffer to account for pipetting volume was not calculate this. My implementation of MasterMixCal bridges this gap by reading recipes for one sample per experiment from a JSON file, 'recipes.json', scaling the recipe by the number of samples multiplied by 1.1 to account for the 10% buffer.

---

## My Contribution
My original files are as follows:
1. 'modules/labplanner/tools/master_mix_calc.py': Master mix calculator function
2. 'modules/labplanner/tools/master_mix_calc.json': MCP wrapper
3. 'modules/labplanner/data/recipes.json': JSON file containing recipes per one reaction
4. 'modules/labplanner/data/instructions.json': Bench instructions for each supported protocol
5. 'tests/test_calculator.py': Pytests writted for master_mix_calc.py

The following files were pre-existing from the BioEng140L project, but modified to integrate the master mix calculator:
1. 'modules/labplanner/140l_code/LabPacketFactory.py': Replaced hardcoded recipes with calls to calculate_master_mix
2. 'modules/labplanner/140l_code/Serializer.py': Updated labels in Lab Packet to 'Scaled Recipes'

The remaining files in the folder labelled '140l_code' were from the previous BioEng140L implementation and were not modified.

---

## MCP Component
The master mix calculator is also an MCP tool that utilized Google Gemini. Some test prompts to utilize the tool after calling 'python client_gemini.py' are as follows:
1. Calculate the master mix for PCR with 10 reactions.
2. How much of each reagent do I need to run the ligate protocol on 4 reactions?
3. Calculate the master mixes for 10 PCR reactions and 3 gibson reactions.
4. How much of each reagent would I need for 15 gibson reactions?

Some test prompts in order to observe edge cases are as follows:
1. What is the master mix of a Golden Gate reaction with 6 samples? 
    - This raise a ValueError, and Gemini should tell you that Golden Gate is not in the recipe book.
2. Calculate the master mix for 0 PCR reactions.
    - This should ValueError, and Gemini should tell you that the number of samples must be a positive number.

## Implementation
The basic project architecture was adopted from the previous developers who created the original LabPlanner codebase. For my individual contribution, the flow is as follows:
1. 'LabPacketFactory' calls 'calculate_master_mix(protocol_name, num_samples)' when building each LabSheet per experiment. 
2. 'MasterMixCalc' looks up the recipes for one reaction per input protocol from 'recipes.json.'
3. Individual reagents in each recipe are scaled by the product of 'num_samples' and 1.1 to account for the 10% buffer.
4. The scaled master mix recipe is converted into a 'Recipe' object and stored in the LabSheet.
5. 'Serializer' writes the scaled recipe into the output lab packets.

### Supported Protocols
Currently, the protocols that are supported by the master mix calculator are as follows:
1. PCR
2. Ligate
3. Gibson

### Running the Python Code
In order to run the python code, move into the 140l_code directory by typing 'cd modules/labplanner/140l_code' from the project root in the terminal.
Then, create a new directory by typing 'mkdir -p out-labpacket out-inventory' in the terminal.
Finally, type 'python main.py' in the terminal.

Output files will be written to 'out-labpacket/' and 'out-inventory/'. This implementation was adopted from the previous developers who created the original LabPlanner codebase in BioEng140L.

### Running Pytests
In order to run the pytests for the calculator, type the following into the terminal from the project root:
'pytest tests/test_calculator.py -v'

___

## Limitations
Currently, my implementation of the mastermix calculator only handles three protocols, and the PCR protocol is one of them. However, I was originally inspired to start this individual scope due to my personal experience with conducting large genotypes with multiple loci (up to 196 samples.) When multiple loci are implemented, we implement different types of PCR protocols, including Tissue-Specific PCR, General PCR, and SNP PCR. In the future, more protocols that benefit from mastermixes, rather than individual pipetting, should be included. 

In addition, the 'digest' and 'golden gate' protocols does not account for the required enzymes, as enzymes vary per  step. Therefore, these enzymes could not be integrated into 'recipes.json.' Therefore, I chose to omit these protocol from the master mix calculator. A future implementation could create a stock of the master mix without the enzymes, aliquot per reaction, then note the individual enzymes needed per reaction. 

Finally, the previous developers also had protocols called transporm, pick, miniprep, gel, and zymo. These steps do not utlize mastermixes, so I chose to exclude them from my calculator.