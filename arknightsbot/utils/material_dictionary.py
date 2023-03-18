from collections import deque

materials_list = ["Aketon",
                  "Bipolar Nanoflake",
                  "Coagulating Gel",
                  "Compound Cutting Fluid",
                  "Crystalline Circuit",
                  "Crystalline Component",
                  "Crystalline Electronic Unit",
                  "Cutting Fluid Solution",
                  "Damaged Device",
                  "D32 Steel",
                  "Device",
                  "Diketon",
                  "Ester",
                  "Grindstone",
                  "Grindstone Pentahydrate",
                  "Incandescent Alloy",
                  "Incandescent Alloy Block",
                  "Integrated Device",
                  "Keton Colloid",
                  "Loxic Kohl",
                  "Manganese Ore",
                  "Manganese Trihydrate",
                  "Oiron",
                  "Oiron Block",
                  "Oiron Cluster",
                  "Oiron Shard",
                  "Orirock",
                  "Orirock Cluster",
                  "Orirock Concentration",
                  "Orirock Cube",
                  "Optimized Device",
                  "Polyester",
                  "Polyester Lump",
                  "Polyester Pack",
                  "Polyketon",
                  "Polymerization Preparation",
                  "Polymerized Gel",
                  "Refined Solvent",
                  "RMA70-12",
                  "RMA70-24",
                  "Semi-Synthetic Solvent",
                  "Sugar",
                  "Sugar Lump",
                  "Sugar Pack",
                  "Sugar Substitute",
                  "White Horse Kohl"]


def optimal_stage_for_material(materials):
    """
    Finds the optimal stage to farm a material
    References: https://gamepress.gg/arknights/sites/arknights/files/2022-10/BestFarmStagesEp10.png

            Parameters:
                    materials: A dictionary containing the name of the material as the key and
                               the number needed as an int value

            Returns:
                    optimal_stages_list: A list of strings of stage names
    """
    materials_to_stages = {
        "ester": ["s2-7"],
        "sugar substitute": ["s2-6"],
        "orirock": ["s2-5"],
        "oriron shard": ["s2-8"],
        "diketon": ["s2-9"],
        "damaged device": ["2-3"],
        "polyester": ["1-8"],
        "sugar": ["5-3"],
        "orirock cube": ["1-7"],
        "oriron": ["5-7"],
        "polyketon": ["7-12"],
        "device": ["6-11"],
        "polyester pack": ["7-4"],
        "sugar pack": ["10-10"],
        "orirock cluster": ["10-6"],
        "oriron cluster": ["5-5"],
        "aketon": ["10-4"],
        "integrated device": ["9-10"],
        "crystalline component": ["r8-11"],
        "loxic kohl": ["4-4"],
        "manganese ore": ["10-7"],
        "RMA70-12": ["4-9"],
        "grindstone": ["4-8"],
        "incandescent alloy": ["10-14"],
        "coagulating gel": ["jt8-2"],
        "compound cutting fluid": ["10-17"],
        "semi-synthetic solvent": ["9-4"]
    }
    optimal_stages_list = {}
    for material, quantity in materials:
        if material in materials_to_stages:
            for stage in materials_to_stages[material]:
                current_material = material
                optimal_stages_list[stage] = optimal_stages_list.get(stage, 0) + quantity
    optimal_stages_list = list(optimal_stages_list.items())
    optimal_stages_list = [(stage, quantity, current_material) for stage, quantity in optimal_stages_list]
    return optimal_stages_list


def calculate_material_equivalency(material, quantity):
    material_equivalencies = {
        "orirock concentration": [(4, "orirock cluster")],
        "orirock cluster": [(5, "orirock cube")],
        "sugar lump": [(2, "sugar pack"), (1, "oriron cluster"), (1, "manganese ore")],
        "polyester lump": [(2, "polyester pack"), (1, "aketon"), (1, "loxic kohl")],
        "oriron block": [(2, "oriron cluster"), (1, "integrated device"), (1, "polyester pack")],
        "keton colloid": [(2, "aketon"), (1, "sugar pack"), (1, "manganese ore")],
        "optimized device": [(1, "integrated device"), (2, "orirock cluster"), (1, "grindstone")],
        "white horse kohl": [(1, "loxic kohl"), (1, "sugar pack"), (1, "rma70-12")],
        "manganese trihydrate": [(2, "manganese ore"), (1, "polyester pack"), (1, "loxic kohl")],
        "grindstone pentahydrate": [(1, "grindstone"), (1, "oriron cluster"), (1, "integrated device")],
        "rma70-24": [(1, "rma70-12"), (2, "orirock cluster"), (1, "aketon")],
        "polymerization preparation": [(1, "orirock concentration"), (1, "oriron block"), (1, "keton colloid")],
        "bipolar nanoflake": [(1, "optimized device"), (2, "white horse kohl")],
        "d32 steel": [(1, "manganese trihydrate"), (1, "grindstone pentahydrate"), (1, "rma70-24")],
        "crystalline electronic unit": [(1, "crystalline circuit"), (2, "polymerized gel"),
                                        (1, "incandescent alloy block")],
        "polymerized gel": [(1, "oriron cluster"), (1, "coagulating gel"), (1, "incandescent alloy")],
        "incandescent alloy block": [(1, "integrated device"), (1, "grindstone"), (1, "incandescent alloy")],
        "crystalline circuit": [(2, "crystalline component"), (1, "coagulating gel"), (1, "incandescent alloy")],
        "refined solvent": [(1, "semi-synthetic solvent"), (1, "compound cutting fluid"), (1, "coagulating gel")],
        "cutting fluid solution": [(1, "compound cutting fluid"), (1, "crystalline component"), (1, "rma70-12")]
    }
    materials = {}
    queue = deque()
    if material in material_equivalencies:
        for item in material_equivalencies[material]:
            materials[item[1]] = item[0] * quantity
            if item[1] in material_equivalencies:
                queue.append((item[1], materials[item[1]]))
    else:
        materials[material] = quantity
    while queue:
        mat, qty = queue.popleft()
        del materials[mat]
        new_materials = calculate_material_equivalency(mat, qty)
        materials.update(new_materials)
        queue.extend((m, new_materials[m]) for m in new_materials if m in material_equivalencies)
    total_materials_list = list(materials.items())
    return total_materials_list
