"""
Class for opponent movement tracking.
Contains variables representing table state
These can be updated by checking the opponent's position
using the lidar. If the opponent passes over plants or pots
we can consider them gone
"""

import asyncio

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional, Tuple

class RegionKind(Enum):
    Unknown = 0
    GrabZone = 1
    DropZone = 2
    OpponentDropZone = 3
    DangerousZone = 4

@dataclass
class RegionOfInterest:
    name: str
    kind: RegionKind
    center: Tuple[float, float]
    radius: float

    enabled: bool = True

    detection_threshold: int = 3

    visited_by_us: bool = False
    visited_by_opponent: bool = False
    detect_cnt: int = 0
    last_seen_opponent_inside: Optional[float] = None

    def contains(self, x: float, y: float) -> bool:
        dx = x - self.center[0]
        dy = y - self.center[1]
        return dx * dx + dy * dy <= self.radius * self.radius

    def check_visiting_state(self):
        if not self.enabled: return

        if lidar.objectInDisk(self.center, self.radius):
            self.detect_cnt = self.detect_cnt + 1
            if self.detect_cnt >= self.detection_threshold:
                self.visited_by_opponent = True

@dataclass
class FieldMonitor:
    regions: dict[str,RegionOfInterest] = field(default_factory=dict)
    scanning: bool = True

    def add_region(self, region):
        self.regions[region.name] = region

    def do_scan(self):
        for reg in self.regions.values():
            reg.check_visiting_state()

    async def run(self):
        print ("FieldMonitor.run()..")
        dbg_cnt = 0
        while self.scanning == True:
            self.do_scan()
            if dbg_cnt==40:
                #print ("MiddleGrabNear visited = {}".format(self.regions["MiddleGrabNear"].visited_by_opponent))
                #print ("MiddleGrabFar visited = {}".format(self.regions["MiddleGrabFar"].visited_by_opponent))
                dbg_cnt = 0
            else:
                dbg_cnt = dbg_cnt + 1
            await asyncio.sleep(0.05)


