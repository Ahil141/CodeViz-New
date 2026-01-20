from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class VisualizationType(str, Enum):
    NONE = "none"
    HTML = "html"
    
    # Specific Data Structures
    STACK = "stack"
    QUEUE = "queue"
    CIRCULAR_QUEUE = "circular_queue"
    DEQUE = "deque"
    ARRAY = "array"
    LINKED_LIST = "linked_list"
    DOUBLY_LINKED_LIST = "doubly_linked_list"
    CIRCULAR_LINKED_LIST = "circular_linked_list"
    BINARY_TREE = "binary_tree"
    HEAP = "heap"
    GRAPH = "graph"
    
    # Algorithms
    SORTING = "sorting"
    SEARCHING = "searching"
    
    # Generic (keep for fallbacks)
    DATA_STRUCTURE = "data_structure"
    ALGORITHM = "algorithm"

class CodeBlock(BaseModel):
    language: str
    code: str
    title: Optional[str] = None

class ChatRequest(BaseModel):
    prompt: str
    history: Optional[List[dict]] = None # For future context support

class ChatResponse(BaseModel):
    text_response: str
    visualization_type: VisualizationType = VisualizationType.NONE
    code_blocks: Optional[List[CodeBlock]] = None
    
    # Metadata used for frontend rendering
    visualization_data: Optional[dict] = None
    
    # New feature: Actual code implementation for the DS/Algo
    implementation_code: Optional[CodeBlock] = None
