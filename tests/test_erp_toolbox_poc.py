import unittest

from scripts.erp_toolbox_poc import compute_summary, evaluate_cost_risks


class ErpToolboxPocTests(unittest.TestCase):
    def test_evaluate_cost_risks_detects_findings(self):
        metrics = {
            "facade_complexity_score": 8.0,
            "glazing_ratio": 0.6,
            "wet_area_count": 7,
            "max_structural_span_m": 8.5,
            "circulation_area_ratio": 0.24,
        }
        findings, missing, active_rules = evaluate_cost_risks(metrics)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(findings), 5)
        self.assertIn("glazing_ratio_max", active_rules)

    def test_evaluate_cost_risks_reports_missing(self):
        findings, missing, _ = evaluate_cost_risks({})
        self.assertEqual(len(findings), 0)
        self.assertGreaterEqual(len(missing), 5)

    def test_compute_summary_levels(self):
        summary = compute_summary([], ["x"])
        self.assertEqual(summary["risk_level"], "low")
        self.assertEqual(summary["risk_score"], 0)

    def test_custom_rules_reduce_findings(self):
        metrics = {
            "facade_complexity_score": 8.0,
            "glazing_ratio": 0.6,
            "wet_area_count": 7,
            "max_structural_span_m": 8.5,
            "circulation_area_ratio": 0.24,
        }
        custom_rules = {
            "facade_complexity_min": 9,
            "glazing_ratio_max": 0.7,
            "wet_area_count_min": 10,
            "max_structural_span_m_max": 9,
            "circulation_area_ratio_max": 0.3,
        }
        findings, missing, _ = evaluate_cost_risks(metrics, custom_rules)
        self.assertEqual(len(missing), 0)
        self.assertEqual(len(findings), 0)


if __name__ == "__main__":
    unittest.main()
