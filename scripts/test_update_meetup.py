"""Unit tests for scripts/update_meetup.py (standard library only).

Run:  python3 -m unittest discover -s scripts -p "test_*.py"
CI runs this in .github/workflows/check-site.yml before the weekly update-meetup job can
publish a wrong date to every page.
"""
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_meetup as um  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


class ThirdSunday(unittest.TestCase):
    def test_known_dates(self):
        expected = {
            (2026, 10): date(2026, 10, 18),
            (2026, 11): date(2026, 11, 15),
            (2026, 12): date(2026, 12, 20),
            (2027, 1): date(2027, 1, 17),
            (2027, 2): date(2027, 2, 21),
            (2027, 3): date(2027, 3, 21),
        }
        for (y, m), d in expected.items():
            self.assertEqual(um.third_sunday(y, m), d)

    def test_always_a_sunday_in_days_15_to_21(self):
        for y in range(2026, 2031):
            for m in range(1, 13):
                d = um.third_sunday(y, m)
                self.assertEqual(d.weekday(), 6, d)
                self.assertTrue(15 <= d.day <= 21, d)


class Upcoming(unittest.TestCase):
    def test_meetup_day_itself_counts_as_upcoming(self):
        self.assertEqual(um.upcoming_third_sundays(1, today=date(2026, 10, 18))[0], date(2026, 10, 18))

    def test_day_after_rolls_to_next_month(self):
        self.assertEqual(um.upcoming_third_sundays(1, today=date(2026, 10, 19))[0], date(2026, 11, 15))

    def test_crosses_year_boundary_in_order(self):
        got = um.upcoming_third_sundays(4, today=date(2026, 11, 16))
        self.assertEqual(got, [date(2026, 12, 20), date(2027, 1, 17), date(2027, 2, 21), date(2027, 3, 21)])


class Formatting(unittest.TestCase):
    def test_banner(self):
        self.assertEqual(um.fmt_banner(date(2026, 11, 15)), "SUNDAY, NOVEMBER 15")

    def test_upper_has_no_leading_zero(self):
        self.assertEqual(um.fmt_upper(date(2027, 3, 7)), "MARCH 7, 2027")


class Ics(unittest.TestCase):
    def setUp(self):
        self.ics = um.build_ics([date(2026, 10, 18), date(2026, 11, 15)])

    def test_one_to_four_pm_eastern_across_dst(self):
        self.assertIn("DTSTART:20261018T170000Z", self.ics)  # EDT
        self.assertIn("DTEND:20261018T200000Z", self.ics)
        self.assertIn("DTSTART:20261115T180000Z", self.ics)  # EST
        self.assertIn("DTEND:20261115T210000Z", self.ics)

    def test_structure_and_line_endings(self):
        self.assertTrue(self.ics.startswith("BEGIN:VCALENDAR\r\n"))
        self.assertTrue(self.ics.endswith("END:VCALENDAR\r\n"))
        self.assertEqual(self.ics.count("BEGIN:VEVENT"), 2)
        self.assertNotIn("\n", self.ics.replace("\r\n", ""))

    def test_lines_folded_to_75_octets(self):
        for line in self.ics.split("\r\n"):
            self.assertLessEqual(len(line.encode("utf-8")), 75, line)

    def test_stable_uids_and_dtstamp(self):
        self.assertIn("UID:2026-10-18-meetup@dmvthrowers.club", self.ics)
        self.assertEqual(self.ics, um.build_ics([date(2026, 10, 18), date(2026, 11, 15)]))

    def test_location_is_escaped(self):
        self.assertIn("LOCATION:Arlington Central Library\\, 1015 N Quincy St\\, Arlington\\, VA 22201", self.ics.replace("\r\n ", ""))


class TopBarOnRealPages(unittest.TestCase):
    """Run the top-bar rewrite on copies of the real pages, so a markup change that breaks
    the regex shows up here instead of silently on the live site."""

    def test_rewrites_index_and_events(self):
        target = date(2026, 11, 15)
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("index.html", "events.html"):
                src = REPO / name
                dst = Path(tmp) / name
                dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                um.update_topbar(dst, target, quiet=True)
                self.assertIn("SUNDAY, NOVEMBER 15", dst.read_text(encoding="utf-8"), name)

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "index.html"
            original = (REPO / "index.html").read_text(encoding="utf-8")
            dst.write_text(original, encoding="utf-8")
            um.update_topbar(dst, date(2027, 6, 20), dry_run=True, quiet=True)
            self.assertEqual(dst.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
