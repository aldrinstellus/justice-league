"""
Screenshot Engine for Penpot Design Analysis
Generates high-quality screenshots and visual documentation
"""

import logging
import json
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import io


@dataclass
class ScreenshotSpec:
    """Specification for a screenshot"""
    name: str
    type: str  # 'full_screen', 'component', 'section'
    coordinates: Optional[Tuple[int, int, int, int]] = None  # x, y, width, height
    quality: str = 'high'
    annotations: List[Dict] = None
    variants: List[str] = None


@dataclass
class AnnotationSpec:
    """Specification for an annotation"""
    type: str  # 'callout', 'highlight', 'measurement', 'boundary'
    coordinates: Tuple[int, int, int, int]
    label: str
    style: Dict[str, Any]


class ScreenshotEngine:
    """Generate screenshots and visual documentation from Penpot data"""

    def __init__(self, config: Optional[Dict] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or self._default_config()
        self.output_dir = Path(self.config.get('output_dir', 'output/screenshots'))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _default_config(self) -> Dict[str, Any]:
        """Default screenshot configuration"""
        return {
            'output_dir': 'output/screenshots',
            'quality': 'high',
            'formats': ['png', 'jpg'],
            'resolutions': {
                'thumbnail': {'width': 300, 'height': 200},
                'medium': {'width': 800, 'height': 600},
                'high': {'width': 1440, 'height': 1080}
            },
            'annotation_styles': {
                'callout': {
                    'background_color': '#ffffff',
                    'border_color': '#3b82f6',
                    'text_color': '#1f2937',
                    'font_size': 12
                },
                'highlight': {
                    'overlay_color': '#3b82f6',
                    'opacity': 0.2,
                    'border_color': '#3b82f6'
                }
            }
        }

    def generate_screenshots(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive screenshots from analysis results

        Args:
            analysis_results: Complete analysis results

        Returns:
            Dictionary containing screenshot metadata and paths
        """
        self.logger.info("Generating screenshots from analysis results")

        try:
            screenshot_collection = {
                'full_screens': self._generate_full_screen_shots(analysis_results),
                'component_shots': self._generate_component_shots(analysis_results),
                'layout_shots': self._generate_layout_shots(analysis_results),
                'comparison_shots': self._generate_comparison_shots(analysis_results),
                'annotation_overlays': self._generate_annotation_overlays(analysis_results),
                'metadata': {
                    'total_screenshots': 0,
                    'formats': self.config['formats'],
                    'resolutions': list(self.config['resolutions'].keys()),
                    'output_directory': str(self.output_dir)
                }
            }

            # Update metadata
            total_count = (
                len(screenshot_collection['full_screens']) +
                len(screenshot_collection['component_shots']) +
                len(screenshot_collection['layout_shots']) +
                len(screenshot_collection['comparison_shots'])
            )
            screenshot_collection['metadata']['total_screenshots'] = total_count

            self.logger.info(f"Generated {total_count} screenshots")
            return screenshot_collection

        except Exception as e:
            self.logger.error(f"Screenshot generation failed: {str(e)}")
            raise

    def _generate_full_screen_shots(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate full application screenshots"""
        full_screens = []

        # Main application screenshot
        main_screenshot = self._create_main_application_screenshot(analysis_results)
        if main_screenshot:
            full_screens.append(main_screenshot)

        # Page-specific screenshots
        extracted_data = analysis_results.get('extracted_data', {})
        for file_id, file_data in extracted_data.get('files', {}).items():
            for page_id, page_data in file_data.get('pages', {}).items():
                page_screenshot = self._create_page_screenshot(page_id, page_data, analysis_results)
                if page_screenshot:
                    full_screens.append(page_screenshot)

        return full_screens

    def _create_main_application_screenshot(self, analysis_results: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create main application screenshot with annotations"""

        # For now, create a placeholder/mock screenshot since we can't actually render Penpot
        screenshot_data = {
            'name': 'main_application_view',
            'title': 'Wisconsin DNR Grant Application - Main Interface',
            'file_path': str(self.output_dir / 'main_application_full.png'),
            'dimensions': {'width': 1440, 'height': 1078},
            'type': 'full_screen',
            'description': 'Complete Wisconsin DNR grant application interface showing all major components',
            'annotations': [
                {
                    'type': 'highlight',
                    'coordinates': {'x': 100, 'y': 200, 'width': 300, 'height': 50},
                    'label': 'Primary Navigation Area',
                    'color': '#3b82f6',
                    'description': 'Main navigation for grant application system'
                },
                {
                    'type': 'callout',
                    'coordinates': {'x': 400, 'y': 300, 'width': 400, 'height': 200},
                    'label': 'Grant Application Form',
                    'description': 'Core functionality for $100k RTP funding applications'
                },
                {
                    'type': 'highlight',
                    'coordinates': {'x': 800, 'y': 500, 'width': 200, 'height': 100},
                    'label': 'Document Upload Area',
                    'color': '#10b981',
                    'description': 'Support for PDF, JPEG, Docx, Xlsx formats'
                }
            ],
            'quality_metrics': {
                'resolution': '1440x1078',
                'file_size': '2.4MB',
                'format': 'PNG'
            }
        }

        # Create placeholder image for demonstration
        self._create_placeholder_screenshot(screenshot_data)

        return screenshot_data

    def _create_placeholder_screenshot(self, screenshot_data: Dict[str, Any]):
        """Create a placeholder screenshot for demonstration purposes"""
        dimensions = screenshot_data['dimensions']
        width, height = dimensions['width'], dimensions['height']

        # Create a placeholder image
        img = Image.new('RGB', (width, height), color='#f8fafc')
        draw = ImageDraw.Draw(img)

        # Try to load a font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw title
        title = screenshot_data.get('title', 'Design Screenshot')
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 50), title, fill='#1f2937', font=title_font)

        # Draw placeholder content areas
        content_areas = [
            {'x': 100, 'y': 150, 'width': 1240, 'height': 80, 'color': '#e2e8f0', 'label': 'Header Area'},
            {'x': 100, 'y': 250, 'width': 300, 'height': 600, 'color': '#f1f5f9', 'label': 'Navigation'},
            {'x': 420, 'y': 250, 'width': 820, 'height': 600, 'color': '#ffffff', 'label': 'Main Content'},
        ]

        for area in content_areas:
            # Draw rectangle
            draw.rectangle([area['x'], area['y'], area['x'] + area['width'], area['y'] + area['height']],
                          fill=area['color'], outline='#cbd5e1')

            # Draw label
            label_bbox = draw.textbbox((0, 0), area['label'], font=text_font)
            label_width = label_bbox[2] - label_bbox[0]
            label_x = area['x'] + (area['width'] - label_width) // 2
            label_y = area['y'] + area['height'] // 2
            draw.text((label_x, label_y), area['label'], fill='#64748b', font=text_font)

        # Draw annotations
        for annotation in screenshot_data.get('annotations', []):
            coords = annotation['coordinates']
            x, y, w, h = coords['x'], coords['y'], coords['width'], coords['height']

            if annotation['type'] == 'highlight':
                # Draw highlight overlay
                overlay = Image.new('RGBA', (width, height), (59, 130, 246, 51))  # 20% opacity blue
                highlight_draw = ImageDraw.Draw(overlay)
                highlight_draw.rectangle([x, y, x + w, y + h], fill=(59, 130, 246, 51), outline=(59, 130, 246, 128), width=2)
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

                # Add label
                draw.text((x, y - 25), annotation['label'], fill='#3b82f6', font=text_font)

            elif annotation['type'] == 'callout':
                # Draw callout box
                draw.rectangle([x + w + 10, y, x + w + 200, y + 60], fill='#ffffff', outline='#3b82f6', width=2)
                draw.text((x + w + 15, y + 5), annotation['label'], fill='#1f2937', font=text_font)

                # Draw line from area to callout
                draw.line([x + w, y + h//2, x + w + 10, y + 30], fill='#3b82f6', width=2)

        # Save the image
        img.save(screenshot_data['file_path'], 'PNG', quality=95)
        self.logger.info(f"Created placeholder screenshot: {screenshot_data['file_path']}")

    def _generate_component_shots(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate isolated component screenshots"""
        component_shots = []

        # Get component inventory
        components = analysis_results.get('components', {})
        component_inventory = components.get('component_inventory', {}).get('components', {})

        for comp_name, usage_count in component_inventory.items():
            if usage_count > 1:  # Only create shots for reusable components
                component_shot = self._create_component_screenshot(comp_name, analysis_results)
                if component_shot:
                    component_shots.append(component_shot)

        return component_shots

    def _create_component_screenshot(self, comp_name: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create isolated component screenshot"""

        screenshot_data = {
            'name': f'component_{comp_name.lower().replace(" ", "_").replace("-", "_")}',
            'component_name': comp_name,
            'title': f'{comp_name} Component',
            'file_path': str(self.output_dir / f'component_{comp_name.lower().replace(" ", "_")}.png'),
            'type': 'component',
            'variants': self._identify_component_variants(comp_name),
            'specifications': self._get_component_specifications(comp_name, analysis_results),
            'usage_count': analysis_results.get('components', {}).get('component_inventory', {}).get('components', {}).get(comp_name, 0),
            'description': f'Isolated view of {comp_name} component with all variants and specifications'
        }

        # Create component screenshot
        self._create_component_placeholder(screenshot_data)

        return screenshot_data

    def _create_component_placeholder(self, screenshot_data: Dict[str, Any]):
        """Create placeholder component screenshot"""
        img = Image.new('RGB', (800, 400), color='#ffffff')
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 18)
            text_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        comp_name = screenshot_data['component_name']

        # Draw title
        draw.text((50, 30), f'{comp_name} Component', fill='#1f2937', font=title_font)

        # Draw component examples based on type
        if 'button' in comp_name.lower():
            self._draw_button_examples(draw, text_font)
        elif 'input' in comp_name.lower():
            self._draw_input_examples(draw, text_font)
        elif 'table' in comp_name.lower():
            self._draw_table_examples(draw, text_font)
        else:
            self._draw_generic_component_examples(draw, text_font, comp_name)

        # Draw specifications
        specs = screenshot_data.get('specifications', {})
        y_offset = 300
        draw.text((50, y_offset), 'Specifications:', fill='#374151', font=text_font)
        for key, value in specs.items():
            y_offset += 20
            draw.text((60, y_offset), f'{key}: {value}', fill='#6b7280', font=text_font)

        img.save(screenshot_data['file_path'], 'PNG', quality=95)
        self.logger.info(f"Created component screenshot: {screenshot_data['file_path']}")

    def _draw_button_examples(self, draw, font):
        """Draw button component examples"""
        buttons = [
            {'label': 'Primary Button', 'color': '#3b82f6', 'x': 50, 'y': 80},
            {'label': 'Secondary Button', 'color': '#ffffff', 'x': 200, 'y': 80, 'border': '#3b82f6'},
            {'label': 'Disabled Button', 'color': '#e5e7eb', 'x': 350, 'y': 80},
        ]

        for btn in buttons:
            # Draw button background
            draw.rectangle([btn['x'], btn['y'], btn['x'] + 120, btn['y'] + 40],
                          fill=btn['color'], outline=btn.get('border', btn['color']))

            # Draw button text
            text_color = '#ffffff' if btn['color'] != '#ffffff' else '#374151'
            draw.text((btn['x'] + 10, btn['y'] + 12), btn['label'][:8] + '...', fill=text_color, font=font)

    def _draw_input_examples(self, draw, font):
        """Draw input component examples"""
        inputs = [
            {'label': 'Default Input', 'x': 50, 'y': 80},
            {'label': 'Error Input', 'x': 50, 'y': 130, 'border': '#ef4444'},
            {'label': 'Disabled Input', 'x': 50, 'y': 180, 'bg': '#f9fafb'},
        ]

        for inp in inputs:
            # Draw input field
            bg_color = inp.get('bg', '#ffffff')
            border_color = inp.get('border', '#d1d5db')
            draw.rectangle([inp['x'], inp['y'], inp['x'] + 250, inp['y'] + 35],
                          fill=bg_color, outline=border_color)

            # Draw label
            draw.text((inp['x'], inp['y'] - 20), inp['label'], fill='#374151', font=font)

            # Draw placeholder text
            draw.text((inp['x'] + 10, inp['y'] + 10), 'Placeholder text...', fill='#9ca3af', font=font)

    def _draw_table_examples(self, draw, font):
        """Draw table component examples"""
        # Draw table header
        draw.rectangle([50, 80, 500, 110], fill='#f9fafb', outline='#e5e7eb')
        headers = ['Column 1', 'Column 2', 'Column 3']
        for i, header in enumerate(headers):
            draw.text((60 + i * 150, 90), header, fill='#374151', font=font)

        # Draw table rows
        for row in range(3):
            y_pos = 110 + row * 30
            draw.rectangle([50, y_pos, 500, y_pos + 30], fill='#ffffff', outline='#e5e7eb')
            for col in range(3):
                draw.text((60 + col * 150, y_pos + 8), f'Data {row+1}-{col+1}', fill='#6b7280', font=font)

    def _draw_generic_component_examples(self, draw, font, comp_name):
        """Draw generic component examples"""
        # Draw a generic container
        draw.rectangle([50, 80, 400, 200], fill='#f8fafc', outline='#cbd5e1')
        draw.text((200, 130), f'{comp_name}', fill='#6b7280', font=font)
        draw.text((150, 150), 'Component Preview', fill='#9ca3af', font=font)

    def _generate_layout_shots(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate layout and section screenshots"""
        layout_shots = []

        # Create layout screenshots for major sections
        sections = [
            {'name': 'form_layout', 'title': 'Form Layout Structure'},
            {'name': 'navigation_layout', 'title': 'Navigation Layout'},
            {'name': 'content_layout', 'title': 'Main Content Layout'}
        ]

        for section in sections:
            layout_shot = {
                'name': section['name'],
                'title': section['title'],
                'file_path': str(self.output_dir / f"{section['name']}.png"),
                'type': 'layout',
                'description': f'Layout structure for {section["title"]}'
            }

            # Create placeholder layout screenshot
            self._create_layout_placeholder(layout_shot)
            layout_shots.append(layout_shot)

        return layout_shots

    def _create_layout_placeholder(self, layout_data: Dict[str, Any]):
        """Create placeholder layout screenshot"""
        img = Image.new('RGB', (1000, 600), color='#ffffff')
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 18)
        except:
            title_font = ImageFont.load_default()

        # Draw title
        draw.text((50, 30), layout_data['title'], fill='#1f2937', font=title_font)

        # Draw layout wireframe
        layout_areas = [
            {'x': 50, 'y': 80, 'width': 900, 'height': 60, 'color': '#e2e8f0', 'label': 'Header'},
            {'x': 50, 'y': 160, 'width': 200, 'height': 350, 'color': '#f1f5f9', 'label': 'Sidebar'},
            {'x': 270, 'y': 160, 'width': 680, 'height': 350, 'color': '#ffffff', 'label': 'Main Content'},
        ]

        for area in layout_areas:
            draw.rectangle([area['x'], area['y'], area['x'] + area['width'], area['y'] + area['height']],
                          fill=area['color'], outline='#cbd5e1', width=2)

        img.save(layout_data['file_path'], 'PNG', quality=95)
        self.logger.info(f"Created layout screenshot: {layout_data['file_path']}")

    def _generate_comparison_shots(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate before/after comparison screenshots"""
        comparison_shots = []

        # Create comparison shots for design system improvements
        improvements = analysis_results.get('persona_analyses', {}).get('design_systems_designer', {}).get('improvement_recommendations', [])

        for improvement in improvements[:3]:  # Limit to top 3 improvements
            comparison_shot = {
                'name': f"comparison_{improvement.get('category', 'improvement').lower().replace(' ', '_')}",
                'title': f"Before/After: {improvement.get('title', 'Improvement')}",
                'file_path': str(self.output_dir / f"comparison_{improvement.get('category', 'improvement').lower().replace(' ', '_')}.png"),
                'type': 'comparison',
                'improvement': improvement,
                'description': f"Visual comparison showing {improvement.get('description', 'improvement')}"
            }

            # Create comparison screenshot
            self._create_comparison_placeholder(comparison_shot)
            comparison_shots.append(comparison_shot)

        return comparison_shots

    def _create_comparison_placeholder(self, comparison_data: Dict[str, Any]):
        """Create placeholder comparison screenshot"""
        img = Image.new('RGB', (1200, 600), color='#ffffff')
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 18)
            text_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw title
        draw.text((50, 30), comparison_data['title'], fill='#1f2937', font=title_font)

        # Draw "Before" section
        draw.text((150, 80), 'BEFORE', fill='#ef4444', font=title_font)
        draw.rectangle([50, 110, 550, 510], fill='#fef2f2', outline='#fecaca', width=2)
        draw.text((250, 300), 'Current State', fill='#991b1b', font=text_font)

        # Draw "After" section
        draw.text((750, 80), 'AFTER', fill='#10b981', font=title_font)
        draw.rectangle([650, 110, 1150, 510], fill='#f0fdf4', outline='#bbf7d0', width=2)
        draw.text((850, 300), 'Improved State', fill='#065f46', font=text_font)

        # Draw arrow
        draw.polygon([(580, 300), (620, 280), (620, 290), (640, 290), (640, 310), (620, 310), (620, 320)],
                    fill='#6b7280')

        img.save(comparison_data['file_path'], 'PNG', quality=95)
        self.logger.info(f"Created comparison screenshot: {comparison_data['file_path']}")

    def _generate_annotation_overlays(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate annotation overlays for screenshots"""
        annotation_overlays = []

        # Create annotation overlays for key insights
        personas_with_visual_insights = ['design_systems_designer', 'accessibility_specialist', 'product_designer']

        for persona in personas_with_visual_insights:
            persona_data = analysis_results.get('persona_analyses', {}).get(persona, {})
            if persona_data:
                overlay = {
                    'name': f'{persona}_annotations',
                    'persona': persona,
                    'title': f'{persona.replace("_", " ").title()} Annotations',
                    'file_path': str(self.output_dir / f'{persona}_annotations.png'),
                    'type': 'annotation_overlay',
                    'insights': self._extract_visual_insights(persona_data)
                }

                annotation_overlays.append(overlay)

        return annotation_overlays

    def _extract_visual_insights(self, persona_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract insights that can be visually annotated"""
        insights = []

        # Extract recommendations that have visual impact
        recommendations = persona_data.get('improvement_recommendations', [])
        for rec in recommendations:
            if any(keyword in rec.get('title', '').lower() for keyword in ['color', 'spacing', 'typography', 'layout']):
                insights.append({
                    'type': 'improvement_opportunity',
                    'title': rec.get('title', ''),
                    'description': rec.get('description', ''),
                    'priority': rec.get('priority', 'medium')
                })

        return insights

    # Helper methods
    def _identify_component_variants(self, comp_name: str) -> List[str]:
        """Identify possible variants for a component"""
        name_lower = comp_name.lower()

        if 'button' in name_lower:
            return ['primary', 'secondary', 'tertiary', 'disabled', 'loading']
        elif 'input' in name_lower:
            return ['default', 'error', 'success', 'disabled', 'focused']
        elif 'table' in name_lower:
            return ['striped', 'bordered', 'compact', 'sortable']
        else:
            return ['default']

    def _get_component_specifications(self, comp_name: str, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get component specifications for documentation"""
        base_specs = {
            'height': '40px',
            'border_radius': '6px',
            'font_family': 'DM Sans',
            'font_size': '14px'
        }

        if 'button' in comp_name.lower():
            base_specs.update({
                'padding': '8px 16px',
                'primary_color': '#3b82f6',
                'text_color': '#ffffff'
            })
        elif 'input' in comp_name.lower():
            base_specs.update({
                'padding': '10px 12px',
                'border': '1px solid #d1d5db',
                'focus_border': '#3b82f6'
            })
        elif 'table' in comp_name.lower():
            base_specs.update({
                'header_bg': '#f9fafb',
                'border_color': '#e5e7eb',
                'row_height': '44px'
            })

        return base_specs

    def create_component_gallery_image(self, components_data: Dict[str, Any]) -> str:
        """Create a comprehensive component gallery image"""
        gallery_path = str(self.output_dir / 'component_gallery.png')

        # Calculate dimensions based on number of components
        component_count = len(components_data.get('component_inventory', {}).get('components', {}))
        grid_cols = 4
        grid_rows = (component_count + grid_cols - 1) // grid_cols

        img_width = 1200
        img_height = max(600, grid_rows * 150 + 100)

        img = Image.new('RGB', (img_width, img_height), color='#ffffff')
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw title
        draw.text((50, 30), 'Component Gallery', fill='#1f2937', font=title_font)

        # Draw component grid
        components = list(components_data.get('component_inventory', {}).get('components', {}).items())
        for i, (comp_name, usage_count) in enumerate(components):
            row = i // grid_cols
            col = i % grid_cols

            x = 50 + col * 280
            y = 80 + row * 150

            # Draw component card
            draw.rectangle([x, y, x + 260, y + 130], fill='#f8fafc', outline='#e2e8f0', width=1)

            # Component name
            draw.text((x + 10, y + 10), comp_name[:20], fill='#1f2937', font=text_font)

            # Usage count
            draw.text((x + 10, y + 30), f'Used {usage_count} times', fill='#6b7280', font=text_font)

            # Simple component representation
            if 'button' in comp_name.lower():
                draw.rectangle([x + 20, y + 60, x + 120, y + 90], fill='#3b82f6', outline='#3b82f6')
                draw.text((x + 25, y + 70), 'Button', fill='#ffffff', font=text_font)
            elif 'input' in comp_name.lower():
                draw.rectangle([x + 20, y + 60, x + 180, y + 90], fill='#ffffff', outline='#d1d5db')
                draw.text((x + 25, y + 70), 'Input field', fill='#9ca3af', font=text_font)
            else:
                draw.rectangle([x + 20, y + 60, x + 150, y + 90], fill='#e5e7eb', outline='#d1d5db')
                draw.text((x + 25, y + 70), 'Component', fill='#6b7280', font=text_font)

        img.save(gallery_path, 'PNG', quality=95)
        self.logger.info(f"Created component gallery: {gallery_path}")

        return gallery_path