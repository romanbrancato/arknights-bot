def split_stage_string(stage_string):
    stage_prefix = ""
    episode = 0
    stage = 0
    parts = stage_string.split('-')
    for char in parts[0]:
        if char.isalpha():
            stage_prefix += char
        elif char.isdigit():
            episode = int(parts[0][len(stage_prefix):])
            break
    stage = int(parts[1])
    return stage_prefix, episode, stage
