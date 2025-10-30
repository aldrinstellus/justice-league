"""Annotation System for visual markup and annotations"""

class AnnotationSystem:
    """Provides visual annotation capabilities for screenshots and reports"""

    def __init__(self):
        self.annotations = []

    def add_annotation(self, element_id, annotation_type, text):
        """Add an annotation to an element"""
        self.annotations.append({
            'element_id': element_id,
            'type': annotation_type,
            'text': text
        })

    def get_annotations(self):
        """Get all annotations"""
        return self.annotations

    def clear_annotations(self):
        """Clear all annotations"""
        self.annotations = []
