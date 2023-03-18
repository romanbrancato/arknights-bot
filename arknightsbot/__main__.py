from arknightsbot.bot.material_farmer import repeat_stage

# Bot assumes that LD instance is named "Arknights_Bot" and Arknights is opened
def main():
    """List of possible arguments you can pass to the repeat stage function.

        FORMAT: repeat_stage(stage_string=None, max_repeats=None, refill=False, target_material=None, target_needed=0)

        stage_string i.e. "1-7" (Must include the quotation marks)
        max_repeats i.e. 7 (No quotation marks)
        refill: if set to True will use all sanity potions. If you only want to refill a few times just use the
                potions before you start
        THE FOLLOWING SHOULD BE USED TOGETHER
        target_material i.e. polyketon or manganese trihydrate (capitalization does not matter)
        target_needed i.e. 3 (No quotation marks)

        repeat_stage() without any parameters will just repeat a stage indefinitely until you are out of sanity\

        You can leave out parameters you are not using i.e. repeat_stage(max_repeats=10)

    """

    repeat_stage(stage_string=None, max_repeats=None, refill=False, target_material=None, target_needed=0)


if __name__ == "__main__":
    main()
