"""
Cross-mapping between NIST SP 800-53 Rev.5, ISO 27001:2022, NIST CSF 2.0, and ISO 27005.

This module provides structured mappings of key NIST 800-53 control families
to their equivalents in other major compliance frameworks, enabling organizations
to understand coverage overlap and gap analysis.
"""

import csv
import io
import json
import os
from typing import Dict, List, Any, Optional

# Path to the SSoT JSON file
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CROSSMAP_PATH = os.path.join(DATA_DIR, "crossmap.json")

def load_crossmap() -> List[Dict[str, Any]]:
    """Load cross-mapping data from JSON."""
    try:
        with open(CROSSMAP_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Fallback or empty if file missing/broken
        return []

CROSSMAP = load_crossmap()

def get_crossmap(
    family: Optional[str] = None,
    nist_id: Optional[str] = None,
    framework: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return filtered cross-mapping data.

    Args:
        family: Filter by NIST control family (e.g. "Access Control")
        nist_id: Filter by specific NIST control ID (e.g. "AC-2")
        framework: Filter to only include a specific target framework
                   ("iso27001", "csf2", "iso27005")
    """
    results = CROSSMAP

    if family:
        family_lower = family.lower()
        results = [r for r in results if family_lower in r["nist_family"].lower()]

    if nist_id:
        nist_upper = nist_id.upper()
        results = [r for r in results if r["nist_id"] == nist_upper]

    if framework and framework in ("iso27001", "csf2", "iso27005"):
        # Slim the output to only the requested framework
        slimmed = []
        for r in results:
            slimmed.append({
                "nist_id": r["nist_id"],
                "nist_title": r["nist_title"],
                "nist_family": r["nist_family"],
                framework: r[framework],
                f"{framework}_titles": r[f"{framework}_titles"],
            })
        return slimmed

    return results


def get_families() -> List[str]:
    """Return list of unique NIST control families in the mapping."""
    seen = set()
    families = []
    for entry in CROSSMAP:
        f = entry["nist_family"]
        if f not in seen:
            seen.add(f)
            families.append(f)
    return families


def get_stats() -> Dict[str, Any]:
    """Return summary statistics about the cross-mapping coverage."""
    families = set()
    iso27001_controls = set()
    csf2_controls = set()
    iso27005_clauses = set()

    for entry in CROSSMAP:
        families.add(entry["nist_family"])
        for c in entry["iso27001"]:
            iso27001_controls.add(c)
        for c in entry["csf2"]:
            csf2_controls.add(c)
        for c in entry["iso27005"]:
            iso27005_clauses.add(c)

    return {
        "total_nist_controls": len(CROSSMAP),
        "nist_families": len(families),
        "unique_iso27001_controls": len(iso27001_controls),
        "unique_csf2_categories": len(csf2_controls),
        "unique_iso27005_clauses": len(iso27005_clauses),
    }


def generate_sankey_csv() -> str:
    """Generate a Sankey diagram CSV with source,target,value columns.

    Produces links from NIST 800-53 controls to their mapped controls in
    ISO 27001, CSF 2.0, and ISO 27005.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["source", "target", "value"])

    for entry in CROSSMAP:
        nist_label = f"NIST {entry['nist_id']}"

        for ctrl in entry["iso27001"]:
            writer.writerow([nist_label, f"ISO {ctrl}", 1])

        for i, cat in enumerate(entry["csf2"]):
            writer.writerow([nist_label, f"CSF {cat}", 1])

        for i, clause in enumerate(entry["iso27005"]):
            writer.writerow([nist_label, f"ISO27005 {clause}", 1])

    return output.getvalue()
