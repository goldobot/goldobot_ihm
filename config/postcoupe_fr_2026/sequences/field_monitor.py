"""
Class for opponent movement tracking.
Contains variables representing table state
These can be updated by checking the opponent's position
using the lidar. If the opponent passes over plants or pots
we can consider them gone
"""

import asyncio


class FieldMonitor:
    roi_0 = True

    _roi_0 = 0

    _detection_threshold = 3

    pose_roi_0 = (1.200, -0.350, 0)

    _scan = True

    def __init__(self):
        self._scan = True

    async def run(self):
        while self._scan == True:
            self.scan()
            await asyncio.sleep(0.02)

    async def scan(self):
        self.check_roi_0()

    async def check_plants_top_left(self):
        if lidar.objectInDisk(self.pose_roi_0, 0.2):
            self._roi_0 = self._roi_0 + 1
            if self._roi_0 >= self._detection_threshold:
                self.roi_0 = False
        else:
            self._roi_0 = 0

