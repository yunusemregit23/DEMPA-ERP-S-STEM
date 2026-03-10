#!/usr/bin/env python3
"""Collect GitHub star/fork stats and (if available) PyPI recent downloads.

Usage:
  python scripts/oss_benchmark.py
"""
from __future__ import annotations
import json
import urllib.request
import urllib.error

REPOS = [
    ("blender/blender", "3B modelleme/render motoru"),
    ("FreeCAD/FreeCAD", "Parametrik CAD/BIM"),
    ("IfcOpenShell/IfcOpenShell", "IFC/BIM işleme"),
    ("mozman/ezdxf", "DXF işleme"),
    ("langchain-ai/langchain", "Ajan orkestrasyonu"),
    ("run-llama/llama_index", "RAG/indeksleme"),
]

PYPI_PACKAGES = ["ifcopenshell", "ezdxf", "langchain", "llama-index"]


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "codex-benchmark-script"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def safe_get(url: str):
    try:
        return get_json(url), None
    except Exception as exc:  # noqa: BLE001
        return None, str(exc)


def main() -> None:
    print("# GitHub Benchmark")
    print("repo\tstars\tforks\tnotes")
    for repo, note in REPOS:
        data, err = safe_get(f"https://api.github.com/repos/{repo}")
        if err:
            print(f"{repo}\tNA\tNA\t{note} | error={err}")
            continue
        print(f"{repo}\t{data.get('stargazers_count')}\t{data.get('forks_count')}\t{note}")

    print("\n# PyPI Recent Downloads (last_month)")
    print("package\tlast_month")
    for pkg in PYPI_PACKAGES:
        data, err = safe_get(f"https://pypistats.org/api/packages/{pkg}/recent")
        if err:
            print(f"{pkg}\tNA ({err})")
            continue
        print(f"{pkg}\t{data['data']['last_month']}")


if __name__ == "__main__":
    main()
