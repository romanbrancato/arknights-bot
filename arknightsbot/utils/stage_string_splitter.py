def split_stage_string(stage_string):
    """
    Splits a given stage name into specific parts.

            Parameters:
                    stage_string (string): A string containing the stage name

            Returns:
                    stage_prefix (string): A string containing all letters in stage name
                    episode (int): An int containing the episode number
                    stage (int): An int containing the stage number
    """
    stage_prefix = ""
    episode = 0
    stage = 0
    parts = stage_string.rsplit("-",1)
    for char in parts[0]:
        if char.isalpha():
            stage_prefix += char
        elif char.isdigit():
            episode = int(parts[0][len(stage_prefix):])
            break
    stage = int(parts[1])
    return stage_prefix, episode, stage
