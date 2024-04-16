import asyncio
import numpy as np

@robot_sequence
async def get_cake_layers():
    count = 0
    if sensors['sick_niveau_1'] == False:
        count = count + 1
        if sensors['sick_niveau_2'] == False:
            count = count + 1
            if sensors['sick_niveau_3'] == False:
                count = count + 1
                if sensors['sick_niveau_4'] == False:
                    count = count + 1
    return count
