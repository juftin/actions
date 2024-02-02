"""
Generate documentation pages for the project.
"""

import logging
import mkdocs_gen_files
from pathlib import Path

logger = logging.getLogger(__name__)

project_dir = Path(__file__).parent.parent
docs_dir = project_dir / ".docs"

readme = project_dir / "README.md"

readme_content = readme.read_text()
with mkdocs_gen_files.open("index.md", "w") as index_file:
    index_file.write(readme_content)
