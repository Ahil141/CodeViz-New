"""
Intent Detection Module for Smart Chat.

Uses the local LLM to classify user messages and determine if they're
asking about data structures, and if so, which one and what operations.
"""

import json
import re
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from app.core.llm import LLM


@dataclass
class Intent:
    """Represents the detected intent from a user message."""
    is_ds_query: bool
    data_structure: Optional[str] = None
    operations: Optional[List[str]] = None
    explanation_needed: bool = True
    raw_message: str = ""


# Mapping from common user terms to database DS names
DS_NAME_MAPPING = {
    # Stacks and Queues
    "stack": "Stack",
    "queue": "Queue",
    
    # Linked Lists
    "linked list": "Singly Linked List",
    "singly linked list": "Singly Linked List",
    "doubly linked list": "Doubly Linked List",
    "circular linked list": "Circular Linked List",
    "circular doubly linked list": "Circular Doubly Linked List",
    "skip list": "Skip List",
    "unrolled linked list": "Unrolled Linked List",
    "xor linked list": "XOR Linked List",
    
    # Arrays
    "array": "Array",
    "arrays": "Array",
    "dynamic array": "Dynamic Array",
    "sparse array": "Sparse Array",
    "jagged array": "Jagged Array",
    "circular array": "Circular Array",
    
    # Trees
    "tree": "General Tree",
    "general tree": "General Tree",
    "binary tree": "Binary Search Tree",
    "bst": "Binary Search Tree",
    "binary search tree": "Binary Search Tree",
    "avl tree": "AVL Tree",
    "avl": "AVL Tree",
    "red black tree": "Red-Black Tree",
    "red-black tree": "Red-Black Tree",
    "splay tree": "Splay Tree",
    "treap": "Treap",
    "scapegoat tree": "Scapegoat Tree",
    
    # Heaps
    "heap": "Max Heap",
    "min heap": "Min Heap",
    "max heap": "Max Heap",
    "binomial heap": "Binomial Heap",
    "fibonacci heap": "Fibonacci Heap",
    "pairing heap": "Pairing Heap",
    
    # B-Trees
    "b tree": "B-Tree",
    "b-tree": "B-Tree",
    "b+ tree": "BPlus Tree",
    "b plus tree": "BPlus Tree",
    "b* tree": "BStar Tree",
    "b star tree": "BStar Tree",
    
    # Graphs
    "graph": "Graph",
    "directed graph": "Graph",
    "undirected graph": "Graph",
    "weighted graph": "Graph",
}

# Known operations for each data structure
DS_OPERATIONS = {
    "Stack": ["push", "pop", "peek", "clear"],
    "Queue": ["enqueue", "dequeue", "peek", "clear"],
    "Singly Linked List": ["insert_front", "insert_end", "delete_front", "delete_end", "search", "traverse"],
    "Doubly Linked List": ["insert_front", "insert_end", "delete_front", "delete_end", "search", "traverse"],
    "Circular Linked List": ["insert_front", "insert_end", "delete_front", "delete_end", "search", "traverse"],
}

# Operation aliases - map user terms to standard operation names
OPERATION_ALIASES = {
    # Stack operations
    "push": "push",
    "add": "push",
    "insert": "push",
    "pop": "pop",
    "remove": "pop",
    "peek": "peek",
    "top": "peek",
    "clear": "clear",
    "empty": "clear",
    
    # Queue operations
    "enqueue": "enqueue",
    "dequeue": "dequeue",
    
    # Linked list operations
    "insert at front": "insert_front",
    "insert front": "insert_front",
    "insert at beginning": "insert_front",
    "add front": "insert_front",
    "insert at end": "insert_end",
    "insert end": "insert_end",
    "insert at back": "insert_end",
    "add end": "insert_end",
    "append": "insert_end",
    "delete front": "delete_front",
    "delete at front": "delete_front",
    "remove front": "delete_front",
    "delete end": "delete_end",
    "delete at end": "delete_end",
    "remove end": "delete_end",
    "search": "search",
    "find": "search",
    "traverse": "traverse",
    "display": "traverse",
    "show": "traverse",
}


INTENT_DETECTION_PROMPT = """You are an intent classifier for a data structure learning application.

Analyze the user's message and determine:
1. Is this a request to learn about or visualize a data structure? (is_ds_query)
2. Which data structure are they asking about? (data_structure)
3. Are they asking about specific operations? (operations)

Respond ONLY with valid JSON in this exact format:
{{
  "is_ds_query": true or false,
  "data_structure": "name" or null,
  "operations": ["op1", "op2"] or null,
  "explanation_needed": true or false
}}

Rules:
- is_ds_query is true if user wants to learn about, visualize, or understand a data structure
- data_structure should be one of: stack, queue, linked list, doubly linked list, array, tree, bst, heap, graph
- operations should list specific operations mentioned (push, pop, insert, delete, search, etc.) or null for all
- explanation_needed is true if user seems to want explanation, false if they just want visualization

Examples:
User: "help me learn stack"
{{"is_ds_query": true, "data_structure": "stack", "operations": null, "explanation_needed": true}}

User: "show me only the push operation in stack"
{{"is_ds_query": true, "data_structure": "stack", "operations": ["push"], "explanation_needed": false}}

User: "what is the capital of France?"
{{"is_ds_query": false, "data_structure": null, "operations": null, "explanation_needed": false}}

User: "explain how insertion works in linked list"
{{"is_ds_query": true, "data_structure": "linked list", "operations": ["insert_front", "insert_end"], "explanation_needed": true}}

User: "visualize queue enqueue and dequeue"
{{"is_ds_query": true, "data_structure": "queue", "operations": ["enqueue", "dequeue"], "explanation_needed": false}}

Now analyze this message:
User: "{user_message}"
"""


class IntentDetector:
    """Detects user intent for data structure learning queries."""
    
    def __init__(self, llm: Optional[LLM] = None):
        """Initialize with an optional LLM instance."""
        self._llm = llm
    
    @property
    def llm(self) -> LLM:
        """Lazy-load LLM instance."""
        if self._llm is None:
            self._llm = LLM()
        return self._llm
    
    def detect(self, message: str) -> Intent:
        """
        Detect the intent from a user message using fast keyword matching.
        
        Args:
            message: The user's message
            
        Returns:
            Intent object with classification results
        """
        # Use fast keyword matching (no LLM needed)
        return self._keyword_detection(message)
    
    def _keyword_detection(self, message: str) -> Intent:
        """Fast keyword-based intent detection."""
        message_lower = message.lower()
        
        # Detect data structure
        detected_ds = None
        
        # Check for specific DS keywords (order matters - more specific first)
        if "linked list" in message_lower or "linkedlist" in message_lower:
            detected_ds = "Singly Linked List"
        elif "stack" in message_lower:
            detected_ds = "Stack"
        elif "queue" in message_lower:
            detected_ds = "Queue"
        elif "array" in message_lower:
            detected_ds = "Array"
        elif "tree" in message_lower or "bst" in message_lower:
            detected_ds = "Binary Search Tree"
        elif "heap" in message_lower:
            detected_ds = "Max Heap"
        elif "graph" in message_lower:
            detected_ds = "Graph"
        
        # If no DS detected, not a DS query
        if not detected_ds:
            return Intent(
                is_ds_query=False,
                raw_message=message
            )
        
        # Detect specific operations based on the data structure
        detected_ops = []
        
        if detected_ds == "Stack":
            if "push" in message_lower or "add" in message_lower or "insert" in message_lower:
                detected_ops.append("push")
            if "pop" in message_lower or "remove" in message_lower:
                detected_ops.append("pop")
            if "peek" in message_lower or "top" in message_lower:
                detected_ops.append("peek")
            if "clear" in message_lower or "empty" in message_lower:
                detected_ops.append("clear")
                
        elif detected_ds == "Queue":
            if "enqueue" in message_lower or "add" in message_lower or "insert" in message_lower:
                detected_ops.append("enqueue")
            if "dequeue" in message_lower or "remove" in message_lower:
                detected_ops.append("dequeue")
            if "peek" in message_lower or "front" in message_lower:
                detected_ops.append("peek")
            if "clear" in message_lower or "empty" in message_lower:
                detected_ops.append("clear")
                
        elif detected_ds == "Singly Linked List":
            if "insert" in message_lower and ("front" in message_lower or "head" in message_lower or "beginning" in message_lower):
                detected_ops.append("insert_front")
            elif "insert" in message_lower and ("end" in message_lower or "tail" in message_lower or "back" in message_lower):
                detected_ops.append("insert_end")
            elif "insert" in message_lower:
                # Generic insert - include both
                detected_ops.extend(["insert_front", "insert_end"])
            
            if "delete" in message_lower or "remove" in message_lower:
                detected_ops.append("delete")
            if "search" in message_lower or "find" in message_lower:
                detected_ops.append("search")
            if "clear" in message_lower:
                detected_ops.append("clear")
        
        return Intent(
            is_ds_query=True,
            data_structure=detected_ds,
            operations=detected_ops if detected_ops else None,
            explanation_needed=True,
            raw_message=message
        )
    
    def _parse_response(self, response: str, original_message: str) -> Intent:
        """Parse the LLM's JSON response into an Intent object."""
        # Try to extract JSON from the response
        try:
            # Find JSON in response (it might have extra text)
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
            
            # Normalize the data structure name
            ds_name = data.get("data_structure")
            if ds_name:
                ds_name = self._normalize_ds_name(ds_name.lower())
            
            # Normalize operations
            operations = data.get("operations")
            if operations and ds_name:
                operations = self._normalize_operations(operations, ds_name)
            
            return Intent(
                is_ds_query=data.get("is_ds_query", False),
                data_structure=ds_name,
                operations=operations,
                explanation_needed=data.get("explanation_needed", True),
                raw_message=original_message
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse LLM response: {e}")
            print(f"Response was: {response}")
            # Fall back to simple detection
            return self._fallback_detection(original_message)
    
    def _normalize_ds_name(self, name: str) -> Optional[str]:
        """Normalize a data structure name to match database entries."""
        name_lower = name.lower().strip()
        return DS_NAME_MAPPING.get(name_lower, name.title())
    
    def _normalize_operations(self, operations: List[str], ds_name: str) -> List[str]:
        """Normalize operation names to standard forms."""
        normalized = []
        for op in operations:
            op_lower = op.lower().strip()
            # Check aliases
            if op_lower in OPERATION_ALIASES:
                normalized.append(OPERATION_ALIASES[op_lower])
            else:
                normalized.append(op_lower.replace(" ", "_"))
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for op in normalized:
            if op not in seen:
                seen.add(op)
                result.append(op)
        
        return result if result else None
    
    def _fallback_detection(self, message: str) -> Intent:
        """Simple keyword-based fallback detection."""
        message_lower = message.lower()
        
        # Check for data structure keywords
        detected_ds = None
        for keyword, ds_name in DS_NAME_MAPPING.items():
            if keyword in message_lower:
                detected_ds = ds_name
                break
        
        if not detected_ds:
            return Intent(
                is_ds_query=False,
                raw_message=message
            )
        
        # Check for operation keywords
        detected_ops = []
        for keyword, op_name in OPERATION_ALIASES.items():
            if keyword in message_lower:
                if op_name not in detected_ops:
                    detected_ops.append(op_name)
        
        return Intent(
            is_ds_query=True,
            data_structure=detected_ds,
            operations=detected_ops if detected_ops else None,
            explanation_needed=True,
            raw_message=message
        )


# Global instance
_intent_detector: Optional[IntentDetector] = None


def get_intent_detector() -> IntentDetector:
    """Get or create the global intent detector instance."""
    global _intent_detector
    if _intent_detector is None:
        _intent_detector = IntentDetector()
    return _intent_detector


def detect_intent(message: str) -> Intent:
    """Convenience function to detect intent from a message."""
    detector = get_intent_detector()
    return detector.detect(message)
