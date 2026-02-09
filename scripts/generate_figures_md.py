#!/usr/bin/env python3
"""
Generate Figures.md with links to all generated figures.

This script scans the figures/ directory and creates a markdown file
with embedded images and descriptions for GitHub viewing.
"""

import os
from pathlib import Path
from datetime import datetime

# Figure descriptions based on filename patterns
FIGURE_DESCRIPTIONS = {
    "polar_motion_raw_timeseries": {
        "title": "Raw Polar Motion Time Series",
        "description": "X and Y components of polar motion from IERS EOP C04 data (1962-present).",
        "category": "Polar Motion",
    },
    "polar_motion_trajectory": {
        "title": "Polar Motion Trajectory",
        "description": "Path of the pole in the x-y plane showing secular drift and wobble.",
        "category": "Polar Motion",
    },
    "polar_motion_detrended": {
        "title": "Detrended Polar Motion",
        "description": "Polar motion with linear trend (secular drift) removed.",
        "category": "Polar Motion",
    },
    "polar_motion_power_spectrum": {
        "title": "Polar Motion Power Spectrum",
        "description": "FFT power spectrum showing peaks at Chandler (~433d) and annual (~365d) periods.",
        "category": "Spectral Analysis",
    },
    "chandler_vs_annual_wobble": {
        "title": "Chandler vs Annual Wobble",
        "description": "Band-pass filtered components isolating Chandler and annual wobbles.",
        "category": "Chandler Wobble",
    },
    "wobble_amplitudes_timeseries": {
        "title": "Wobble Amplitude Evolution",
        "description": "Time series of Chandler and annual wobble amplitudes (smoothed).",
        "category": "Chandler Wobble",
    },
    "chandler_wobble_trajectory": {
        "title": "Chandler Wobble Trajectory",
        "description": "Isolated Chandler wobble motion in the x-y plane.",
        "category": "Chandler Wobble",
    },
    "chandler_phase_analysis": {
        "title": "Chandler Phase Analysis",
        "description": "Phase evolution and residuals from expected 433-day period.",
        "category": "Chandler Wobble",
    },
    "lod_timeseries": {
        "title": "Length of Day Time Series",
        "description": "LOD variations from IERS EOP C04 data.",
        "category": "LOD Analysis",
    },
    "lod_aam_correlation": {
        "title": "LOD-AAM Correlation",
        "description": "Correlation between Length of Day and Atmospheric Angular Momentum.",
        "category": "LOD Analysis",
    },
}


def get_figure_info(filename: str) -> dict:
    """Get title and description for a figure based on its filename."""
    stem = Path(filename).stem

    # Try exact match first
    if stem in FIGURE_DESCRIPTIONS:
        return FIGURE_DESCRIPTIONS[stem]

    # Try partial match
    for key, info in FIGURE_DESCRIPTIONS.items():
        if key in stem:
            return info

    # Default fallback
    title = stem.replace("_", " ").title()
    return {
        "title": title,
        "description": f"Generated figure: {filename}",
        "category": "Other",
    }


def generate_figures_md(figures_dir: str = "figures", output_file: str = "Figures.md") -> None:
    """Generate Figures.md with links to all figures."""
    figures_path = Path(figures_dir)

    if not figures_path.exists():
        print(f"Figures directory '{figures_dir}' does not exist. Creating empty Figures.md")
        with open(output_file, "w") as f:
            f.write("# Generated Figures\n\n")
            f.write("No figures have been generated yet. Run the notebooks to generate figures.\n")
        return

    # Find all image files
    image_extensions = {".png", ".jpg", ".jpeg", ".svg", ".gif"}
    figures = sorted(
        [f for f in figures_path.iterdir() if f.suffix.lower() in image_extensions],
        key=lambda x: x.name,
    )

    # Find CSV/MD summary files
    data_files = sorted(
        [f for f in figures_path.iterdir() if f.suffix.lower() in {".csv", ".md"}],
        key=lambda x: x.name,
    )

    # Group figures by category
    categories: dict = {}
    for fig in figures:
        info = get_figure_info(fig.name)
        category = info["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append((fig, info))

    # Generate markdown
    lines = [
        "# Generated Figures",
        "",
        f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*",
        "",
        "This document contains figures generated from the analysis notebooks.",
        "",
        "## Table of Contents",
        "",
    ]

    # Add TOC
    for category in sorted(categories.keys()):
        anchor = category.lower().replace(" ", "-")
        lines.append(f"- [{category}](#{anchor})")

    if data_files:
        lines.append("- [Data Files](#data-files)")

    lines.append("")

    # Add figures by category
    for category in sorted(categories.keys()):
        lines.append(f"## {category}")
        lines.append("")

        for fig, info in categories[category]:
            lines.append(f"### {info['title']}")
            lines.append("")
            lines.append(info["description"])
            lines.append("")
            lines.append(f"![{info['title']}]({fig})")
            lines.append("")

    # Add data files section
    if data_files:
        lines.append("## Data Files")
        lines.append("")
        lines.append("Summary data files generated by the analysis:")
        lines.append("")
        for f in data_files:
            lines.append(f"- [{f.name}]({f})")
        lines.append("")

    # Write output
    with open(output_file, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated {output_file} with {len(figures)} figures in {len(categories)} categories")


if __name__ == "__main__":
    generate_figures_md()
