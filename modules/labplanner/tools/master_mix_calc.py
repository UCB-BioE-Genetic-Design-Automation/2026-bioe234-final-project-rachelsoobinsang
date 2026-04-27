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
        instructions_path = os.path.join(base_path, "..", "data", "instructions.json")

        try:
            with open(recipe_path, 'r') as f:
                self.recipe_book = json.load(f)
                
        except FileNotFoundError:
            self.recipe_book = {}
            raise FileNotFoundError(f"Could not find recipes.json.")
        
        try:
            with open(instructions_path, 'r') as f:
                self.instruction_book = json.load(f)
                
        except FileNotFoundError:
            self.instruction_book = {}
            raise FileNotFoundError(f"Could not find instructions.json.")
        
    def calculate(self, protocol_name:str, num_samples:int) -> dict:
        lookup_name = protocol_name.replace(" ", "_")
        available = ", ".join(self.recipe_book.keys())
        if lookup_name not in self.recipe_book:
            raise ValueError(f"'{lookup_name} not in the recipe book. Select from: {available}")
        if num_samples <= 0:
            raise ValueError(f"The number of samples must be at least 1.")
        
        base_recipe = self.recipe_book[lookup_name]

        multiplier = num_samples * 1.1

        scaled_recipe = {
            reagent: round(volume * multiplier, 2)
            for reagent, volume in base_recipe.items()
        }

        instruction = self.instruction_book.get(
            lookup_name,
            "Mix reagents for {Samples} samples: {scaled_recipe}"
        )

        fill_data = {**scaled_recipe, "Samples":num_samples}
        new_instructions = instruction.format(**fill_data)

        return {
            "Protocol" : lookup_name,
            "Samples" : num_samples,
            "Scaled Recipe" : scaled_recipe,
            "Instructions": new_instructions,
            "Units" : "uL",
            "Note": f"This recipe accounts for a 10% buffer for pipetting error."
        }

    def run(self, cf_name: str) -> list:
            """
            Processes a Construction File and returns a LabPacket.
            """
            base_path = os.path.dirname(os.path.abspath(__file__))
            cf_path = os.path.join(base_path, "..", "data", "construction_files", cf_name)
            
            if not os.path.exists(cf_path):
                raise FileNotFoundError(f"Construction file not found at {cf_path}")
                
            with open(cf_path, 'r') as f:
                cf_data = json.load(f)
            
            lab_packet = []
            for step in cf_data.get("steps", []):
                result = self.calculate(step["protocol"], step["samples"])
                lab_packet.append(result)
                
            return lab_packet
    
_instance = MasterMixCalc()
_instance.initiate()
calculate_master_mix = _instance.run


if __name__ == "__main__":
    print("--- Starting Local LabPlanner Test ---")
    try:
        # Run the Construction File
        print("\nTesting 'run' with construction file 'ifg1_germline.json'...")
        cf_results = _instance.run("ifg1_germline.json")
        
        # Pretty-print the actual return object (The LabPacket)
        import json
        print("\n--- ACTUAL CF RETURN (LABPACKET) ---")
        print(json.dumps(cf_results, indent=4))

    except Exception as e:
        print(f"\nTEST FAILED: {e}")

