import unittest
from neurobot.simulation import SurgicalToyWorld
from neurobot.brain import CognitiveBrain

class NeuroBotTests(unittest.TestCase):
    def test_world_rejects_obstacle(self):
        world=SurgicalToyWorld()
        world.position=(3,2)
        event=world.move((1,0))
        self.assertEqual(event["event"],"blocked")
        self.assertEqual(world.position,(3,2))

    def test_planner_reaches_target(self):
        world=SurgicalToyWorld(); brain=CognitiveBrain()
        for _ in range(200):
            if world.at_target(): break
            event=world.move(brain.plan_next(world))
            self.assertNotEqual(event["event"],"blocked")
        self.assertTrue(world.at_target())

    def test_memory_records_events(self):
        world=SurgicalToyWorld(); brain=CognitiveBrain()
        event=world.move((1,0))
        brain.remember(world.snapshot(),event)
        self.assertEqual(len(brain.episodic_memory),1)

if __name__=="__main__": unittest.main()
