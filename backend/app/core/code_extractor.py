"""
Code Extractor Module.

Extracts specific operations from visualizer HTML/CSS/JS code
based on operation markers in the code.
"""

import re
from typing import List, Optional, Tuple


class CodeExtractor:
    """Extracts specific operations from visualizer code."""
    
    # Markers used to identify operation boundaries
    OPERATION_START_PATTERN = r'// === OPERATION: (\w+) ==='
    OPERATION_END_PATTERN = r'// === END: (\w+) ==='
    
    def __init__(self):
        pass
    
    def extract_operations(
        self,
        html_code: str,
        operations: List[str],
        keep_core: bool = True
    ) -> str:
        """
        Extract only specified operations from the visualizer code.
        
        Args:
            html_code: Full HTML/CSS/JS visualizer code
            operations: List of operation names to keep
            keep_core: Whether to always keep 'core' operations (like updateDisplay)
            
        Returns:
            Modified HTML with only the specified operations
        """
        if not operations:
            return html_code
        
        # Always include 'core' functions
        ops_to_keep = set(operations)
        if keep_core:
            ops_to_keep.add('core')
        
        # Extract the script section
        script_match = re.search(r'<script>(.*?)</script>', html_code, re.DOTALL)
        if not script_match:
            return html_code
        
        script_content = script_match.group(1)
        
        # Find all operation blocks
        operation_blocks = self._find_operation_blocks(script_content)
        
        if not operation_blocks:
            # No markers found, return original code
            return html_code
        
        # Build new script with only selected operations
        new_script = self._build_filtered_script(script_content, operation_blocks, ops_to_keep)
        
        # Replace script in HTML
        new_html = html_code[:script_match.start(1)] + new_script + html_code[script_match.end(1):]
        
        # Update HTML to hide buttons for removed operations
        new_html = self._update_html_buttons(new_html, operations)
        
        return new_html
    
    def _find_operation_blocks(self, script_content: str) -> List[Tuple[str, int, int]]:
        """
        Find all operation blocks in the script.
        
        Returns:
            List of tuples: (operation_name, start_index, end_index)
        """
        blocks = []
        
        # Find all start markers
        for match in re.finditer(self.OPERATION_START_PATTERN, script_content):
            op_name = match.group(1)
            start_idx = match.start()
            
            # Find corresponding end marker
            end_pattern = f'// === END: {op_name} ==='
            end_match = re.search(re.escape(end_pattern), script_content[start_idx:])
            
            if end_match:
                end_idx = start_idx + end_match.end()
                blocks.append((op_name, start_idx, end_idx))
        
        return blocks
    
    def _build_filtered_script(
        self,
        script_content: str,
        operation_blocks: List[Tuple[str, int, int]],
        ops_to_keep: set
    ) -> str:
        """Build a new script with only the selected operation blocks."""
        
        # Sort blocks by start position
        sorted_blocks = sorted(operation_blocks, key=lambda x: x[1])
        
        # Find content that's not in any operation block (to keep)
        result_parts = []
        last_end = 0
        
        for op_name, start_idx, end_idx in sorted_blocks:
            # Add content before this block
            before_content = script_content[last_end:start_idx].strip()
            if before_content:
                result_parts.append(before_content)
            
            # Add this block if it should be kept
            if op_name in ops_to_keep:
                block_content = script_content[start_idx:end_idx]
                result_parts.append(block_content)
            
            last_end = end_idx
        
        # Add any remaining content after the last block
        remaining = script_content[last_end:].strip()
        if remaining:
            result_parts.append(remaining)
        
        return '\n'.join(result_parts)
    
    def _update_html_buttons(self, html: str, operations: List[str]) -> str:
        """
        Update HTML to hide buttons for operations that were removed.
        This is a simple approach that adds display:none to buttons.
        """
        # Map of operation names to button text patterns
        operation_to_button = {
            'push': r'Push',
            'pop': r'Pop',
            'peek': r'Peek',
            'clear': r'Clear',
            'enqueue': r'Enqueue',
            'dequeue': r'Dequeue',
            'insert_front': r'Insert.*Front|Add.*Front',
            'insert_end': r'Insert.*End|Add.*End|Append',
            'delete_front': r'Delete.*Front|Remove.*Front',
            'delete_end': r'Delete.*End|Remove.*End',
            'search': r'Search|Find',
            'traverse': r'Traverse|Display',
        }
        
        # For each button that should be hidden, add style
        # This is a simple approach - in reality we might want a more sophisticated solution
        # For now, we'll just return the HTML as-is since hiding buttons requires
        # careful analysis of each visualizer's HTML structure
        
        return html
    
    def has_operation_markers(self, html_code: str) -> bool:
        """Check if the code has operation markers."""
        script_match = re.search(r'<script>(.*?)</script>', html_code, re.DOTALL)
        if not script_match:
            return False
        
        script_content = script_match.group(1)
        return bool(re.search(self.OPERATION_START_PATTERN, script_content))
    
    def list_operations(self, html_code: str) -> List[str]:
        """List all operations defined in the visualizer code."""
        script_match = re.search(r'<script>(.*?)</script>', html_code, re.DOTALL)
        if not script_match:
            return []
        
        script_content = script_match.group(1)
        operations = []
        
        for match in re.finditer(self.OPERATION_START_PATTERN, script_content):
            op_name = match.group(1)
            if op_name != 'core':
                operations.append(op_name)
        
        return operations


# Global instance
_code_extractor: Optional[CodeExtractor] = None


def get_code_extractor() -> CodeExtractor:
    """Get or create the global code extractor instance."""
    global _code_extractor
    if _code_extractor is None:
        _code_extractor = CodeExtractor()
    return _code_extractor


def extract_operations(html_code: str, operations: List[str]) -> str:
    """Convenience function to extract operations from visualizer code."""
    extractor = get_code_extractor()
    return extractor.extract_operations(html_code, operations)
