"""Linking System for cross-references and deep linking"""

class LinkingSystem:
    """Manages cross-references and deep links between design elements"""

    def __init__(self):
        self.links = {}

    def add_link(self, source_id, target_id, link_type='reference'):
        """Add a link between elements"""
        if source_id not in self.links:
            self.links[source_id] = []
        self.links[source_id].append({
            'target': target_id,
            'type': link_type
        })

    def get_links(self, source_id):
        """Get links for a specific element"""
        return self.links.get(source_id, [])

    def get_all_links(self):
        """Get all links"""
        return self.links
