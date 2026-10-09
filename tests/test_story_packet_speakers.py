"""Future story packets must leave narrator-only close-ups silent."""
import runpy
import sys
import unittest
from unittest.mock import patch


class StoryPacketSpeakerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with patch.object(sys, "argv", ["production/story_packet.py", "stories/ugly_duckling_v1/packet_source.py"]):
            cls.packet = runpy.run_path("production/story_packet.py", run_name="story_packet_test")

    def one_shot(self, sid):
        source = self.packet["S"]
        with patch.object(source, "SHOTS", [x for x in source.SHOTS if x[0] == sid]), \
             patch.object(source, "LINES", [x for x in source.LINES if sid in x[4]]):
            _, refs = self.packet["foundation"]()
            return self.packet["scenes"](refs)

    def test_narrator_only_closeup_has_no_mouth_variant(self):
        records, shots = self.one_shot("s03_ollie_alone")
        self.assertEqual([v["mode"] for v in shots[0]["variants"]], ["closed"])
        self.assertFalse(any(r.get("mouth_character") for r in records))

    def test_character_closeup_has_closed_boundaries_and_named_anchor(self):
        records, shots = self.one_shot("s06_ottie_closeup")
        mouth = next(v for v in shots[0]["variants"] if v["mode"] == "mouth")
        self.assertEqual(mouth["speaker"], "OTTIE")
        self.assertEqual(mouth["end_image"], shots[0]["end_image"])
        self.assertEqual(mouth["mouth_open_image"], "s06_ottie_closeup_open")
        anchor = next(r for r in records if r["id"] == mouth["mouth_open_image"])
        self.assertEqual(anchor["mouth_character"], "ottie")


if __name__ == "__main__":
    unittest.main()
