def optimal_stage_for_material(material):
    materials_to_stages = {
        "ester": ["s2-7"],
        "sugar_substitute": ["s2-6"],
        "orirock": ["s2-5"],
        "oriron_shard": ["s2-8"],
        "diketon": ["s2-9"],
        "damaged_device": ["2-3"],
        "polyester": ["1-8"],
        "sugar": ["5-3"],
        "orirock_cube": ["1-7"],
        "oriron": ["5-7"],
        "polyketon": ["7-12", "s2-1"],
        "device": ["6-11", "s3-4"],
        "polyester_pack": ["7-4", "3-8"],
        "sugar_pack": ["10-10"],
        "orirock_cluster": ["10-6"],
        "oriron_cluster": ["5-5"],
        "aketon": ["10-4"],
        "integrated_device": ["9-10", "7-15", "4-10"],
        "crystalline_component": ["r8-11", "s5-9"],
        "loxic_kohl": ["4-4"],
        "manganese_ore": ["10-7", "4-7"],
        "RMA70-12": ["4-9"],
        "grindstone": ["4-8"],
        "incandescent_alloy": ["10-14", "s3-6"],
        "coagulating_gel": ["jt8-2", "s5-7", "7-8"],
        "compound_cutting_fluid": ["10-17", "9-6"],
        "semi-synthetic_solvent": ["9-4"]
    }
    optimal_stages_list = materials_to_stages.get(material)
    return optimal_stages_list

