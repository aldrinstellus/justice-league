"""
Penpot File Extractor
Handles extraction and parsing of Penpot design files
"""

import json
import zipfile
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging


class PenpotExtractor:
    """Extract and parse Penpot design files (.penpot are ZIP archives)"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def extract_penpot_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract and parse a Penpot file

        Args:
            file_path: Path to .penpot file

        Returns:
            Dictionary containing extracted and parsed data
        """
        self.logger.info(f"Extracting Penpot file: {file_path}")

        if not Path(file_path).exists():
            raise FileNotFoundError(f"Penpot file not found: {file_path}")

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Create temporary extraction directory
                extract_dir = Path(file_path).parent / f"temp_extract_{uuid.uuid4().hex[:8]}"
                extract_dir.mkdir(exist_ok=True)

                # Extract all files
                zip_ref.extractall(extract_dir)

                # Parse extracted data
                extracted_data = self._parse_extracted_files(extract_dir)

                # Clean up temporary directory
                self._cleanup_temp_dir(extract_dir)

                return extracted_data

        except Exception as e:
            self.logger.error(f"Failed to extract Penpot file: {str(e)}")
            raise

    def _parse_extracted_files(self, extract_dir: Path) -> Dict[str, Any]:
        """Parse extracted Penpot files"""
        data = {
            'manifest': None,
            'files': {},
            'pages': {},
            'components': {},
            'total_objects': 0,
            'extraction_metadata': {
                'source_path': str(extract_dir.parent),
                'extracted_files_count': 0
            }
        }

        # Parse manifest.json
        manifest_path = extract_dir / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                data['manifest'] = json.load(f)
                self.logger.info(f"Loaded manifest for {data['manifest'].get('files', [{}])[0].get('name', 'Unknown')}")

        # Parse files directory
        files_dir = extract_dir / "files"
        if files_dir.exists():
            data['files'] = self._parse_files_directory(files_dir)

        # Count total objects
        data['total_objects'] = self._count_total_objects(data)

        # Get file count
        data['extraction_metadata']['extracted_files_count'] = len(list(extract_dir.rglob("*.json")))

        return data

    def _parse_files_directory(self, files_dir: Path) -> Dict[str, Any]:
        """Parse the files directory structure"""
        files_data = {}

        for file_dir in files_dir.iterdir():
            if file_dir.is_dir():
                file_id = file_dir.name
                file_data = self._parse_single_file(file_dir)
                files_data[file_id] = file_data

        return files_data

    def _parse_single_file(self, file_dir: Path) -> Dict[str, Any]:
        """Parse a single file directory"""
        file_data = {
            'id': file_dir.name,
            'metadata': None,
            'pages': {},
            'objects_count': 0
        }

        # Parse main file metadata
        main_file = file_dir / f"{file_dir.name}.json"
        if main_file.exists():
            with open(main_file, 'r') as f:
                file_data['metadata'] = json.load(f)

        # Parse pages directory
        pages_dir = file_dir / "pages"
        if pages_dir.exists():
            file_data['pages'] = self._parse_pages_directory(pages_dir)

        # Count objects in this file
        file_data['objects_count'] = sum(
            len(page.get('objects', {})) for page in file_data['pages'].values()
        )

        return file_data

    def _parse_pages_directory(self, pages_dir: Path) -> Dict[str, Any]:
        """Parse pages directory"""
        pages_data = {}

        for page_dir in pages_dir.iterdir():
            if page_dir.is_dir():
                page_id = page_dir.name
                page_data = self._parse_single_page(page_dir)
                pages_data[page_id] = page_data

        return pages_data

    def _parse_single_page(self, page_dir: Path) -> Dict[str, Any]:
        """Parse a single page directory"""
        page_data = {
            'id': page_dir.name,
            'metadata': None,
            'objects': {},
            'object_types': {},
            'components_used': set()
        }

        # Parse page metadata if exists
        page_metadata_file = page_dir / f"{page_dir.name}.json"
        if page_metadata_file.exists():
            with open(page_metadata_file, 'r') as f:
                page_data['metadata'] = json.load(f)

        # Parse all object files in the page
        for object_file in page_dir.glob("*.json"):
            if object_file.name != f"{page_dir.name}.json":  # Skip page metadata
                object_id = object_file.stem
                try:
                    with open(object_file, 'r') as f:
                        object_data = json.load(f)
                        page_data['objects'][object_id] = object_data

                        # Track object types
                        obj_type = object_data.get('type', 'unknown')
                        page_data['object_types'][obj_type] = page_data['object_types'].get(obj_type, 0) + 1

                        # Track component usage
                        component_name = object_data.get('name', '')
                        if component_name and ('V1-' in component_name or 'component' in component_name.lower()):
                            page_data['components_used'].add(component_name)

                except Exception as e:
                    self.logger.warning(f"Failed to parse object file {object_file}: {str(e)}")

        # Convert set to list for JSON serialization
        page_data['components_used'] = list(page_data['components_used'])

        return page_data

    def _count_total_objects(self, data: Dict[str, Any]) -> int:
        """Count total objects across all files and pages"""
        total = 0
        for file_data in data['files'].values():
            total += file_data.get('objects_count', 0)
        return total

    def _cleanup_temp_dir(self, temp_dir: Path):
        """Clean up temporary extraction directory"""
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            self.logger.warning(f"Failed to cleanup temp directory {temp_dir}: {str(e)}")

    def get_file_summary(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the extracted file"""
        manifest = extracted_data.get('manifest', {})
        files = extracted_data.get('files', {})

        # Get first file info (most Penpot files have one main file)
        first_file = next(iter(files.values())) if files else {}

        return {
            'file_name': manifest.get('files', [{}])[0].get('name', 'Unknown'),
            'version': first_file.get('metadata', {}).get('version', 'Unknown'),
            'total_files': len(files),
            'total_pages': sum(len(file_data.get('pages', {})) for file_data in files.values()),
            'total_objects': extracted_data.get('total_objects', 0),
            'features_used': manifest.get('files', [{}])[0].get('features', []),
            'generated_by': manifest.get('generatedBy', 'Unknown'),
            'export_source': manifest.get('referer', 'Unknown')
        }

    def extract_text_content(self, extracted_data: Dict[str, Any]) -> List[str]:
        """Extract all text content from the design file"""
        text_content = []

        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for obj_data in page_data.get('objects', {}).values():
                    if obj_data.get('type') == 'text':
                        content = obj_data.get('content', {})
                        if isinstance(content, dict) and 'children' in content:
                            text = self._extract_text_from_children(content['children'])
                            if text.strip():
                                text_content.append(text.strip())

                    # Also check object names
                    name = obj_data.get('name', '')
                    if name and name not in ['Text', 'Frame'] and not name.startswith('692df9ea-'):
                        text_content.append(name)

        return text_content

    def _extract_text_from_children(self, children: List) -> str:
        """Recursively extract text from content children"""
        text = ""
        for child in children:
            if isinstance(child, dict):
                if child.get('type') == 'text':
                    text += child.get('text', '')
                elif 'children' in child:
                    text += self._extract_text_from_children(child['children'])
        return text

    def get_component_inventory(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get inventory of all components used in the design"""
        component_inventory = {
            'components': {},
            'component_types': {},
            'reusable_components': [],
            'one_off_elements': []
        }

        for file_data in extracted_data.get('files', {}).values():
            for page_data in file_data.get('pages', {}).values():
                for component_name in page_data.get('components_used', []):
                    if component_name in component_inventory['components']:
                        component_inventory['components'][component_name] += 1
                    else:
                        component_inventory['components'][component_name] = 1

                # Analyze object types
                for obj_type, count in page_data.get('object_types', {}).items():
                    if obj_type in component_inventory['component_types']:
                        component_inventory['component_types'][obj_type] += count
                    else:
                        component_inventory['component_types'][obj_type] = count

        # Classify components
        for name, usage_count in component_inventory['components'].items():
            if usage_count > 1:
                component_inventory['reusable_components'].append({
                    'name': name,
                    'usage_count': usage_count
                })
            else:
                component_inventory['one_off_elements'].append(name)

        return component_inventory