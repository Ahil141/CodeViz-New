from app.schemas.chat import VisualizationType
import re

class VisualizationService:
    def __init__(self):
        # Keywords that trigger specific visualization types
        self.html_keywords = [
            "html", "css", "website", "web page", "frontend", "react", "component", "ui"
        ]
        
        # KEYWORD MAPPINGS for Specific Types
        self.type_keywords = {
            VisualizationType.STACK: ["stack", "lifo"],
            VisualizationType.QUEUE: ["queue", "fifo"],
            VisualizationType.CIRCULAR_QUEUE: ["circular queue", "ring buffer"],
            VisualizationType.DEQUE: ["deque", "double ended queue"],
            VisualizationType.ARRAY: ["array", "list", "vector"],
            VisualizationType.LINKED_LIST: ["linked list", "singly linked list"],
            VisualizationType.DOUBLY_LINKED_LIST: ["doubly linked list"],
            VisualizationType.CIRCULAR_LINKED_LIST: ["circular linked list"],
            VisualizationType.BINARY_TREE: ["binary tree", "bst", "binary search tree"],
            VisualizationType.HEAP: ["heap", "priority queue", "max heap", "min heap"],
            VisualizationType.GRAPH: ["graph", "bfs", "dfs", "dijkstra", "network"],
            VisualizationType.SORTING: ["sort", "bubble", "merge", "quick", "insertion", "selection"],
            VisualizationType.SEARCHING: ["search", "binary search", "linear search"]
        }

    def determine_visualization_type(self, prompt: str, response_text: str) -> VisualizationType:
        """
        Analyzes the user prompt and LLM response to decide if a visualization is needed.
        Returns the most relevant VisualizationType.
        """
        text_to_analyze = (prompt + " " + response_text).lower()

        # 1. Check for specific Data Structures / Algorithms first (Specific > Generic)
        for vis_type, keywords in self.type_keywords.items():
            for keyword in keywords:
                if keyword in text_to_analyze:
                    # Special Case: 'list' is generic, so only match if prompt explicitly asks for "linked list" logic or if context implies it
                    # But for now, simple matching is better than none.
                    # Exception: "Linked List" should not match "List" (Array) erroneously without logic?
                    # Python string 'in' checks simple substring. "linked list" contains "list".
                    # Fix: Check specific keys first (longest length)?
                    # The iteration order of dict is insertion order in Python 3.7+.
                    # We defined specific ones (Linked List) after Array. Ideally we check longer phrases first?
                    # Actually, simple check:
                    return vis_type

        # 2. Check for HTML/Frontend intent (Fallback if no specific DS found but 'html' mentioned)
        if any(keyword in text_to_analyze for keyword in self.html_keywords):
            return VisualizationType.HTML

        return VisualizationType.NONE

visualization_service = VisualizationService()
