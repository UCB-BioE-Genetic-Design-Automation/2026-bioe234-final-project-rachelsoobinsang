import json
import os

class MasterMixCalc:
    """
    Description: Calculates volumes needed to create a master mix, including a 10% surplus of\
    the exact needed volume.
    Input: 
    Protocol: String name of specific protocol in recipe book.
    Number of Samples: Integer number of samples in experiment.
    Output:
    Multiplied Recipe: Dictionary of scaled ingredients and volumed needed to carry out experiment.
    """

    def initiate(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        recipe_path = os.path.join(base_path, "..", "data", "recipes.json")

        try:
            with open(recipe_path, 'r') as f:
                self.recipe_book = json.load(f)
        except FileNotFoundError:
            self.recipe_book = {}
            raise FileNotFoundError(f"Could not find recipes.json.")
        
    def run(self, protocol_name:str, num_samples:int) -> dict:
        if protocol_name not in self.recipe_book:
            raise ValueError(f"'{protocol_name} not in the recipe book.")
        if num_samples <= 0:
            raise ValueError(f"The number of samples must be at least 1.")
        
        base_recipe = self.recipe_book[protocol_name]

        multiplier = num_samples * 1.1

        scaled_recipe = {
            reagent: volume * multiplier
            for reagent, volume in base_recipe.items()
        }

        return {
            "Protocol" : protocol_name,
            "Samples" : num_samples,
            "Scaled Recipe" : scaled_recipe,
            "Units" : "uL"
        }
    
_instance = MasterMixCalc()
_instance.initiate()
calculate_master_mix = _instance.run
