"""
Cross-mapping between NIST SP 800-53 Rev.5, ISO 27001:2022, NIST CSF 2.0, and ISO 27005.

This module provides structured mappings of key NIST 800-53 control families
to their equivalents in other major compliance frameworks, enabling organizations
to understand coverage overlap and gap analysis.
"""

import csv
import io
from typing import Dict, List, Any, Optional


# ---------------------------------------------------------------------------
# Cross-Mapping Data
# Each entry maps a NIST 800-53 control to its counterparts in:
#   - ISO 27001:2022 (Annex A controls)
#   - NIST CSF 2.0 (Functions/Categories)
#   - ISO 27005 (Risk Management clauses)
# ---------------------------------------------------------------------------

CROSSMAP: List[Dict[str, Any]] = [
    # --- Access Control (AC) ---
    {
        "nist_id": "AC-1",
        "nist_title": "Policy and Procedures",
        "nist_family": "Access Control",
        "iso27001": ["A.5.1", "A.5.2"],
        "iso27001_titles": ["Policies for information security", "Information security roles and responsibilities"],
        "csf2": ["GV.PO-01"],
        "csf2_titles": ["Organizational context for cybersecurity risk management is established"],
        "iso27005": ["5.1"],
        "iso27005_titles": ["General — Establishing context"],
    },
    {
        "nist_id": "AC-2",
        "nist_title": "Account Management",
        "nist_family": "Access Control",
        "iso27001": ["A.5.16", "A.5.18"],
        "iso27001_titles": ["Identity management", "Access rights"],
        "csf2": ["PR.AA-01", "PR.AA-03"],
        "csf2_titles": ["Identities and credentials are issued", "Users, services, and hardware are authenticated"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    {
        "nist_id": "AC-3",
        "nist_title": "Access Enforcement",
        "nist_family": "Access Control",
        "iso27001": ["A.5.15", "A.8.3"],
        "iso27001_titles": ["Access control", "Information access restriction"],
        "csf2": ["PR.AA-05"],
        "csf2_titles": ["Access permissions and authorizations are managed"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    {
        "nist_id": "AC-6",
        "nist_title": "Least Privilege",
        "nist_family": "Access Control",
        "iso27001": ["A.5.15", "A.8.2"],
        "iso27001_titles": ["Access control", "Privileged access rights"],
        "csf2": ["PR.AA-05"],
        "csf2_titles": ["Access permissions and authorizations are managed"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    {
        "nist_id": "AC-7",
        "nist_title": "Unsuccessful Logon Attempts",
        "nist_family": "Access Control",
        "iso27001": ["A.8.5"],
        "iso27001_titles": ["Secure authentication"],
        "csf2": ["PR.AA-03"],
        "csf2_titles": ["Users, services, and hardware are authenticated"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    # --- Audit and Accountability (AU) ---
    {
        "nist_id": "AU-2",
        "nist_title": "Event Logging",
        "nist_family": "Audit and Accountability",
        "iso27001": ["A.8.15"],
        "iso27001_titles": ["Logging"],
        "csf2": ["DE.CM-09"],
        "csf2_titles": ["Computing hardware and software are monitored"],
        "iso27005": ["8.4"],
        "iso27005_titles": ["Risk evaluation"],
    },
    {
        "nist_id": "AU-3",
        "nist_title": "Content of Audit Records",
        "nist_family": "Audit and Accountability",
        "iso27001": ["A.8.15"],
        "iso27001_titles": ["Logging"],
        "csf2": ["DE.CM-09"],
        "csf2_titles": ["Computing hardware and software are monitored"],
        "iso27005": ["8.4"],
        "iso27005_titles": ["Risk evaluation"],
    },
    {
        "nist_id": "AU-6",
        "nist_title": "Audit Record Review, Analysis, and Reporting",
        "nist_family": "Audit and Accountability",
        "iso27001": ["A.8.15", "A.8.16"],
        "iso27001_titles": ["Logging", "Monitoring activities"],
        "csf2": ["DE.AE-02", "DE.AE-06"],
        "csf2_titles": ["Potentially adverse events are analyzed", "Information on adverse events is provided to authorized staff"],
        "iso27005": ["8.4"],
        "iso27005_titles": ["Risk evaluation"],
    },
    # --- Configuration Management (CM) ---
    {
        "nist_id": "CM-2",
        "nist_title": "Baseline Configuration",
        "nist_family": "Configuration Management",
        "iso27001": ["A.8.9"],
        "iso27001_titles": ["Configuration management"],
        "csf2": ["PR.PS-01"],
        "csf2_titles": ["Configuration management practices are established"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    {
        "nist_id": "CM-6",
        "nist_title": "Configuration Settings",
        "nist_family": "Configuration Management",
        "iso27001": ["A.8.9"],
        "iso27001_titles": ["Configuration management"],
        "csf2": ["PR.PS-01"],
        "csf2_titles": ["Configuration management practices are established"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    {
        "nist_id": "CM-7",
        "nist_title": "Least Functionality",
        "nist_family": "Configuration Management",
        "iso27001": ["A.8.9", "A.8.19"],
        "iso27001_titles": ["Configuration management", "Installation of software on operational systems"],
        "csf2": ["PR.PS-01"],
        "csf2_titles": ["Configuration management practices are established"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    # --- Identification and Authentication (IA) ---
    {
        "nist_id": "IA-2",
        "nist_title": "Identification and Authentication (Organizational Users)",
        "nist_family": "Identification and Authentication",
        "iso27001": ["A.5.16", "A.8.5"],
        "iso27001_titles": ["Identity management", "Secure authentication"],
        "csf2": ["PR.AA-01", "PR.AA-03"],
        "csf2_titles": ["Identities and credentials are issued", "Users, services, and hardware are authenticated"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    {
        "nist_id": "IA-5",
        "nist_title": "Authenticator Management",
        "nist_family": "Identification and Authentication",
        "iso27001": ["A.5.17"],
        "iso27001_titles": ["Authentication information"],
        "csf2": ["PR.AA-02"],
        "csf2_titles": ["Identities are proofed and bound to credentials"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    # --- Incident Response (IR) ---
    {
        "nist_id": "IR-1",
        "nist_title": "Policy and Procedures",
        "nist_family": "Incident Response",
        "iso27001": ["A.5.24"],
        "iso27001_titles": ["Information security incident management planning and preparation"],
        "csf2": ["RS.MA-01"],
        "csf2_titles": ["The incident response plan is executed"],
        "iso27005": ["10.1"],
        "iso27005_titles": ["General — Continual improvement"],
    },
    {
        "nist_id": "IR-4",
        "nist_title": "Incident Handling",
        "nist_family": "Incident Response",
        "iso27001": ["A.5.25", "A.5.26"],
        "iso27001_titles": ["Assessment and decision on information security events", "Response to information security incidents"],
        "csf2": ["RS.MA-02", "RS.AN-03"],
        "csf2_titles": ["Incident reports are triaged and validated", "Analysis is performed to establish what has taken place"],
        "iso27005": ["10.1"],
        "iso27005_titles": ["General — Continual improvement"],
    },
    {
        "nist_id": "IR-6",
        "nist_title": "Incident Reporting",
        "nist_family": "Incident Response",
        "iso27001": ["A.5.24", "A.6.8"],
        "iso27001_titles": ["Information security incident management planning and preparation", "Information security event reporting"],
        "csf2": ["RS.CO-02"],
        "csf2_titles": ["Internal and external stakeholders are notified"],
        "iso27005": ["10.1"],
        "iso27005_titles": ["General — Continual improvement"],
    },
    # --- Risk Assessment (RA) ---
    {
        "nist_id": "RA-3",
        "nist_title": "Risk Assessment",
        "nist_family": "Risk Assessment",
        "iso27001": ["A.5.7"],
        "iso27001_titles": ["Threat intelligence"],
        "csf2": ["ID.RA-01", "ID.RA-02"],
        "csf2_titles": ["Vulnerabilities in assets are identified", "Cyber threat intelligence is received"],
        "iso27005": ["8.2", "8.3", "8.4"],
        "iso27005_titles": ["Risk identification", "Risk analysis", "Risk evaluation"],
    },
    {
        "nist_id": "RA-5",
        "nist_title": "Vulnerability Monitoring and Scanning",
        "nist_family": "Risk Assessment",
        "iso27001": ["A.8.8"],
        "iso27001_titles": ["Management of technical vulnerabilities"],
        "csf2": ["ID.RA-01"],
        "csf2_titles": ["Vulnerabilities in assets are identified"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    # --- System and Communications Protection (SC) ---
    {
        "nist_id": "SC-7",
        "nist_title": "Boundary Protection",
        "nist_family": "System and Communications Protection",
        "iso27001": ["A.8.20", "A.8.21"],
        "iso27001_titles": ["Networks security", "Security of network services"],
        "csf2": ["PR.DS-10"],
        "csf2_titles": ["The confidentiality, integrity, and availability of data-in-transit is protected"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    {
        "nist_id": "SC-8",
        "nist_title": "Transmission Confidentiality and Integrity",
        "nist_family": "System and Communications Protection",
        "iso27001": ["A.8.24"],
        "iso27001_titles": ["Use of cryptography"],
        "csf2": ["PR.DS-10"],
        "csf2_titles": ["The confidentiality, integrity, and availability of data-in-transit is protected"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    {
        "nist_id": "SC-12",
        "nist_title": "Cryptographic Key Establishment and Management",
        "nist_family": "System and Communications Protection",
        "iso27001": ["A.8.24"],
        "iso27001_titles": ["Use of cryptography"],
        "csf2": ["PR.DS-10"],
        "csf2_titles": ["The confidentiality, integrity, and availability of data-in-transit is protected"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    # --- System and Information Integrity (SI) ---
    {
        "nist_id": "SI-2",
        "nist_title": "Flaw Remediation",
        "nist_family": "System and Information Integrity",
        "iso27001": ["A.8.8", "A.8.19"],
        "iso27001_titles": ["Management of technical vulnerabilities", "Installation of software on operational systems"],
        "csf2": ["PR.PS-02"],
        "csf2_titles": ["Software is maintained, replaced, and removed"],
        "iso27005": ["9.1"],
        "iso27005_titles": ["Risk treatment — General"],
    },
    {
        "nist_id": "SI-3",
        "nist_title": "Malicious Code Protection",
        "nist_family": "System and Information Integrity",
        "iso27001": ["A.8.7"],
        "iso27001_titles": ["Protection against malware"],
        "csf2": ["DE.CM-09"],
        "csf2_titles": ["Computing hardware and software are monitored"],
        "iso27005": ["8.3"],
        "iso27005_titles": ["Risk analysis"],
    },
    {
        "nist_id": "SI-4",
        "nist_title": "System Monitoring",
        "nist_family": "System and Information Integrity",
        "iso27001": ["A.8.16"],
        "iso27001_titles": ["Monitoring activities"],
        "csf2": ["DE.CM-01", "DE.CM-09"],
        "csf2_titles": ["Networks and network services are monitored", "Computing hardware and software are monitored"],
        "iso27005": ["8.4", "10.1"],
        "iso27005_titles": ["Risk evaluation", "General — Continual improvement"],
    },
    # --- Planning (PL) ---
    {
        "nist_id": "PL-2",
        "nist_title": "System Security and Privacy Plans",
        "nist_family": "Planning",
        "iso27001": ["A.5.1"],
        "iso27001_titles": ["Policies for information security"],
        "csf2": ["GV.PO-01"],
        "csf2_titles": ["Organizational context for cybersecurity risk management is established"],
        "iso27005": ["5.1"],
        "iso27005_titles": ["General — Establishing context"],
    },
    # --- Contingency Planning (CP) ---
    {
        "nist_id": "CP-2",
        "nist_title": "Contingency Plan",
        "nist_family": "Contingency Planning",
        "iso27001": ["A.5.29", "A.5.30"],
        "iso27001_titles": ["Information security during disruption", "ICT readiness for business continuity"],
        "csf2": ["RC.RP-01"],
        "csf2_titles": ["The recovery portion of the incident response plan is executed"],
        "iso27005": ["9.1"],
        "iso27005_titles": ["Risk treatment — General"],
    },
    {
        "nist_id": "CP-9",
        "nist_title": "System Backup",
        "nist_family": "Contingency Planning",
        "iso27001": ["A.8.13"],
        "iso27001_titles": ["Information backup"],
        "csf2": ["PR.DS-11"],
        "csf2_titles": ["Backups of data are created, protected, maintained, and tested"],
        "iso27005": ["9.1"],
        "iso27005_titles": ["Risk treatment — General"],
    },
    # --- Personnel Security (PS) ---
    {
        "nist_id": "PS-3",
        "nist_title": "Personnel Screening",
        "nist_family": "Personnel Security",
        "iso27001": ["A.6.1"],
        "iso27001_titles": ["Screening"],
        "csf2": ["GV.RR-02"],
        "csf2_titles": ["Roles, responsibilities, and authorities related to cybersecurity risk management are established"],
        "iso27005": ["5.1"],
        "iso27005_titles": ["General — Establishing context"],
    },
    # --- Physical and Environmental Protection (PE) ---
    {
        "nist_id": "PE-2",
        "nist_title": "Physical Access Authorizations",
        "nist_family": "Physical and Environmental Protection",
        "iso27001": ["A.7.1", "A.7.2"],
        "iso27001_titles": ["Physical security perimeters", "Physical entry"],
        "csf2": ["PR.AA-05"],
        "csf2_titles": ["Access permissions and authorizations are managed"],
        "iso27005": ["8.2"],
        "iso27005_titles": ["Risk identification"],
    },
    # --- Security Assessment (CA) ---
    {
        "nist_id": "CA-2",
        "nist_title": "Control Assessments",
        "nist_family": "Security Assessment and Authorization",
        "iso27001": ["A.5.35", "A.5.36"],
        "iso27001_titles": ["Independent review of information security", "Compliance with policies, rules and standards"],
        "csf2": ["ID.RA-04"],
        "csf2_titles": ["Potential impacts and likelihoods of threats exploiting vulnerabilities are identified"],
        "iso27005": ["8.4"],
        "iso27005_titles": ["Risk evaluation"],
    },
    {
        "nist_id": "CA-7",
        "nist_title": "Continuous Monitoring",
        "nist_family": "Security Assessment and Authorization",
        "iso27001": ["A.5.36", "A.8.16"],
        "iso27001_titles": ["Compliance with policies, rules and standards", "Monitoring activities"],
        "csf2": ["DE.CM-01", "DE.CM-09"],
        "csf2_titles": ["Networks and network services are monitored", "Computing hardware and software are monitored"],
        "iso27005": ["10.1"],
        "iso27005_titles": ["General — Continual improvement"],
    },
]


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
