Sync=0
Heartbeat=1
Reset=2
CommStats=3
DbgPrintf=4
DbgGPIO=5
DbgEvent=6

PropulsionTelemetry=8
PropulsionTelemetryEx=9
PropulsionStateChange=10

StartOfMatch=16
EndOfMatch=17

CmdEmergencyStop=32
CmdSelectSide=33
CmdEnterDebugMode=34
CmdExitDebugMode=35

DbgGetOdometryConfig=64
DbgSetOdometryConfig=65
DbgGetPropulsionConfig=66
DbgSetPropulsionConfig=67


DbgDynamixelsList=72
DbgDynamixelDescr=73
DbgDynamixelSetTorqueEnable=74
DbgDynamixelSetGoalPosition=75
DbgDynamixelSetTorqueLimit=76
DbgDynamixelGetRegisters=77
DbgDynamixelSetRegisters=78

DbgSetMotorsEnable=80
DbgSetMotorsPwm=81
DbgSetPropulsionEnable=82
DbgPropulsionSetPose=83
DbgPropulsionTest=84
DbgPropulsionExecuteTrajectory=85
DbgPropulsionExecuteRotation=86
DbgPropulsionExecuteReposition=87
DbgMiscRepositionStartGreen=100
DbgReset=127

DbgArmsSetPose=160
DbgArmsSetCommand=161
DbgArmsSetTorques=162
DbgArmsSetSequences=163
DbgArmsExecuteSequence=164
DbgArmsGoToPosition=165

DbgRobotSetCommand=176
DbgRobotSetPoint=177
DbgRobotSetSequence=178
DbgRobotExecuteSequence=179
DbgRobotSetTrajectoryPoint=180

DbgRobotEnterManualMode=192
DbgRobotExitManualMode=193

FpgaGetVersion=256
FpgaDbgReadReg=257
FpgaDbgWriteReg=258
FpgaCmdServo=272
FpgaCmdDCMotor=288
FpgaCmdPumpR=289
FpgaCmdPumpL=290
FpgaCmdConveyorBelt=291
FpgaCmdStepper=304
FpgaGetStepperPos=305
FpgaColumnsCalib=320
FpgaColumnsMove=321
FpgaColumnsSetOffset=322

GyroDbgReadReg=342
GyroGetAngle=344
GyroDbgWriteReg=376

# Debug event types

DbgEventRobotHoming=0
DbgEventStartMatch=1
DbgEventStartSequence=2
DbgEventExecuteCommand=3
DbgEventGoWaypoint=4
