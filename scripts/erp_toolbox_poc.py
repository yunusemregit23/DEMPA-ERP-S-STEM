#!/usr/bin/env python3
"""ERP Mühendis AI için maliyet/karmaşıklık uyarı motoru PoC.

Bu script CAD/BIM parser değildir; parser çıktısından gelecek özet metriklerle
maliyet riski uyarıları üretir.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Any

SEVERITY_WEIGHTS = {"low": 1, "medium": 2, "high": 3}
DEFAULT_RULES = {
    "facade_complexity_min": 7.0,
    "glazing_ratio_max": 0.55,
    "wet_area_count_min": 6.0,
    "max_structural_span_m_max": 8.0,
    "circulation_area_ratio_max": 0.22,
}


@dataclass
class RuleResult:
    rule: str
    severity: str
    reason: str
    suggestion: str


def _get_float(data: dict[str, Any], key: str) -> float | None:
    val = data.get(key)
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _merge_rules(override_rules: dict[str, Any] | None) -> dict[str, float]:
    rules = dict(DEFAULT_RULES)
    if not override_rules:
        return rules

    for key, val in override_rules.items():
        if key in rules:
            try:
                rules[key] = float(val)
            except (TypeError, ValueError):
                continue
    return rules


def evaluate_cost_risks(
    metrics: dict[str, Any], rule_overrides: dict[str, Any] | None = None
) -> tuple[list[RuleResult], list[str], dict[str, float]]:
    """Verilen proje metriklerine göre maliyet artıran riskleri değerlendirir."""
    results: list[RuleResult] = []
    missing: list[str] = []
    rules = _merge_rules(rule_overrides)

    facade_complexity = _get_float(metrics, "facade_complexity_score")
    if facade_complexity is None:
        missing.append("facade_complexity_score")
    elif facade_complexity >= rules["facade_complexity_min"]:
        results.append(
            RuleResult(
                rule="Cephe karmaşıklığı",
                severity="high",
                reason="Yüksek cephe kırıklılığı/özel detay üretimi işçilik ve kalıp maliyetini artırır.",
                suggestion="Cephe modül tekrarını artır; özel detay oranını düşür.",
            )
        )

    glazing_ratio = _get_float(metrics, "glazing_ratio")
    if glazing_ratio is None:
        missing.append("glazing_ratio")
    elif glazing_ratio > rules["glazing_ratio_max"]:
        results.append(
            RuleResult(
                rule="Cam oranı",
                severity="medium",
                reason="Yüksek cam oranı cephe, doğrama ve iklimlendirme maliyetini yükseltebilir.",
                suggestion="Cephede opak/pencere dengesini iklim ve maliyet hedefiyle optimize et.",
            )
        )

    wet_areas = _get_float(metrics, "wet_area_count")
    if wet_areas is None:
        missing.append("wet_area_count")
    elif wet_areas >= rules["wet_area_count_min"]:
        results.append(
            RuleResult(
                rule="Islak hacim sayısı",
                severity="medium",
                reason="Tesisat hatlarının artması toplam maliyeti ve bakım karmaşıklığını artırır.",
                suggestion="Islak hacim kümelenmesi ile tesisat omurgasını kısalt.",
            )
        )

    max_span = _get_float(metrics, "max_structural_span_m")
    if max_span is None:
        missing.append("max_structural_span_m")
    elif max_span > rules["max_structural_span_m_max"]:
        results.append(
            RuleResult(
                rule="Taşıyıcı açıklık",
                severity="high",
                reason="Büyük açıklıklar kesit ve donatı ihtiyacını artırarak karkas maliyetini büyütür.",
                suggestion="Açıklıkları azaltacak aks düzeni veya hibrit taşıyıcı çözüm değerlendir.",
            )
        )

    circulation_ratio = _get_float(metrics, "circulation_area_ratio")
    if circulation_ratio is None:
        missing.append("circulation_area_ratio")
    elif circulation_ratio > rules["circulation_area_ratio_max"]:
        results.append(
            RuleResult(
                rule="Sirkülasyon oranı",
                severity="low",
                reason="Fazla sirkülasyon alanı satılabilir/kullanılabilir alan verimini düşürebilir.",
                suggestion="Koridor ve çekirdek konumunu yeniden düzenleyerek net alanı artır.",
            )
        )

    return results, sorted(set(missing)), rules


def compute_summary(results: list[RuleResult], missing: list[str]) -> dict[str, Any]:
    score = sum(SEVERITY_WEIGHTS.get(item.severity, 0) for item in results)
    if score >= 8:
        level = "critical"
    elif score >= 5:
        level = "high"
    elif score >= 2:
        level = "medium"
    else:
        level = "low"

    return {
        "risk_score": score,
        "risk_level": level,
        "finding_count": len(results),
        "missing_count": len(missing),
    }


def render_markdown_report(
    project_name: str,
    results: list[RuleResult],
    missing: list[str],
    summary: dict[str, Any],
    active_rules: dict[str, float],
) -> str:
    lines = [
        f"# ERP Maliyet Risk Raporu – {project_name}",
        "",
        "## Özet",
        f"- Risk skoru: **{summary['risk_score']}**",
        f"- Risk seviyesi: **{summary['risk_level'].upper()}**",
        f"- Bulgu sayısı: **{summary['finding_count']}**",
        f"- Eksik veri sayısı: **{summary['missing_count']}**",
        "",
        "## Aktif eşik kuralları",
    ]

    for key, value in active_rules.items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(["", "## Bulgular"])

    if not results:
        lines.append("- Tanımlı kurallara göre yüksek etkili bir maliyet riski bulunmadı.")
    else:
        for item in results:
            lines.append(
                f"- [{item.severity.upper()}] **{item.rule}**: {item.reason} Öneri: {item.suggestion}"
            )

    lines.append("")
    lines.append("## Eksik veri")
    if not missing:
        lines.append("- Eksik veri yok.")
    else:
        lines.append("- " + ", ".join(missing))
        lines.append("- Not: Eksik veriler tamamlanmadan karar önerisi nihai kabul edilmemelidir.")

    return "\n".join(lines) + "\n"


def build_json_report(
    project_name: str,
    results: list[RuleResult],
    missing: list[str],
    summary: dict[str, Any],
    active_rules: dict[str, float],
) -> dict[str, Any]:
    return {
        "project_name": project_name,
        "summary": summary,
        "active_rules": active_rules,
        "findings": [asdict(item) for item in results],
        "missing_metrics": missing,
        "note": "Eksik veriler tamamlanmadan karar önerisi nihai kabul edilmemelidir.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="ERP maliyet risk PoC")
    parser.add_argument("input", help="Proje metrikleri JSON dosyası")
    parser.add_argument("--output", help="Rapor dosya yolu")
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Rapor formatı (varsayılan: md)",
    )
    parser.add_argument(
        "--rules",
        help="Kural eşikleri için JSON dosyası (opsiyonel)",
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    project_name = str(payload.get("project_name", "Adsız Proje"))
    metrics = payload.get("metrics", {})
    if not isinstance(metrics, dict):
        raise SystemExit("metrics alanı JSON nesnesi olmalıdır")

    rule_overrides: dict[str, Any] | None = None
    if args.rules:
        with open(args.rules, "r", encoding="utf-8") as f:
            parsed = json.load(f)
        if not isinstance(parsed, dict):
            raise SystemExit("rules dosyası JSON nesnesi olmalıdır")
        rule_overrides = parsed

    results, missing, active_rules = evaluate_cost_risks(metrics, rule_overrides)
    summary = compute_summary(results, missing)

    if args.format == "json":
        content = json.dumps(
            build_json_report(project_name, results, missing, summary, active_rules),
            ensure_ascii=False,
            indent=2,
        )
    else:
        content = render_markdown_report(project_name, results, missing, summary, active_rules)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
            if args.format == "json":
                f.write("\n")
    else:
        print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
