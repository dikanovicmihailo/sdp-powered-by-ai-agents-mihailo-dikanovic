"""Sphinx configuration file for Kata documentation."""

# -- Project information -----------------------------------------------------
project = "Mars Rover"
copyright = "2026, Mihailo Dikanovic"
author = "Mihailo Dikanovic"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_wagtail_theme",
    "myst_parser",
    "sphinx_new_tab_link",
]

new_tab_link_show_external_link_icon = True

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_wagtail_theme"

html_theme_options = {
    "project_name": "Mars Rover",
    "github_url": "https://github.com/dikanovicmihailo/sdp-powered-by-ai-agents-mihailo-dikanovic",
    "footer_links": "",
}

html_show_copyright = True
html_last_updated_fmt = "%b %d, %Y"
html_show_sphinx = False

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]
