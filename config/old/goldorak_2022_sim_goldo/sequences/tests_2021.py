@robot.sequence
async def test_ferme_pavillon():
    await servos.setEnable('fanion', True)
    await servos.move('fanion', fanion_ferme)

@robot.sequence
async def test_ouvre_pavillon():
    await servos.setEnable('fanion', True)
    await servos.move('fanion', fanion_ouvert)
    await sleep(2)
    await servos.move('fanion', fanion_ferme)