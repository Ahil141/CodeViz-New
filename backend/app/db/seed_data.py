"""
Seed script to insert interactive data structure visualizers into ChromaDB.
Run this script directly: python -m app.db.seed_data
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.db.chroma_store import get_chroma_store


from app.core.visualizers import *



def seed_visualizers():
    """Seed ChromaDB with data structure visualizers."""
    print("Starting to seed visualizers into ChromaDB...")
    
    store = get_chroma_store()
    
    # Prepare documents with metadata
    documents = [
        STACK_VISUALIZER,
        QUEUE_VISUALIZER,
        LINKED_LIST_VISUALIZER,
        DOUBLY_LINKED_LIST_VISUALIZER,
        CIRCULAR_LINKED_LIST_VISUALIZER,
        CIRCULAR_DOUBLY_LINKED_LIST_VISUALIZER,
        SKIP_LIST_VISUALIZER,
        UNROLLED_LINKED_LIST_VISUALIZER,
        XOR_LINKED_LIST_VISUALIZER,
        ARRAY_VISUALIZER,
        DYNAMIC_ARRAY_VISUALIZER,
        SPARSE_ARRAY_VISUALIZER,
        JAGGED_ARRAY_VISUALIZER,
        CIRCULAR_ARRAY_VISUALIZER,
        GENERAL_TREE_VISUALIZER,
        BST_VISUALIZER, # Binary Search Tree
        AVL_TREE_VISUALIZER,
        RED_BLACK_TREE_VISUALIZER,
        SPLAY_TREE_VISUALIZER,
        TREAP_VISUALIZER,
        SCAPEGOAT_TREE_VISUALIZER,
        B_TREE_VISUALIZER,
        B_PLUS_TREE_VISUALIZER,
        B_STAR_TREE_VISUALIZER,
        HEAP_VISUALIZER, # Covers Min/Max
        FIBONACCI_HEAP_VISUALIZER,
        BINOMIAL_HEAP_VISUALIZER,
        PAIRING_HEAP_VISUALIZER,
        UNIFIED_GRAPH_VISUALIZER
    ]
    
    metadatas = [
        {"name": "Stack", "type": "visualizer", "data_structure": "stack", "description": "Interactive Stack visualizer"},
        {"name": "Queue", "type": "visualizer", "data_structure": "queue", "description": "Interactive Queue visualizer"},
        {"name": "Singly Linked List", "type": "visualizer", "data_structure": "singly_linked_list", "description": "Interactive Singly Linked List"},
        
        {"name": "Doubly Linked List", "type": "visualizer", "data_structure": "doubly_linked_list", "description": "Interactive Doubly Linked List"},
        {"name": "Circular Linked List", "type": "visualizer", "data_structure": "circular_linked_list", "description": "Interactive Circular Linked List"},
        {"name": "Circular Doubly Linked List", "type": "visualizer", "data_structure": "circular_doubly_linked_list", "description": "Interactive Circular Doubly Linked List"},
        {"name": "Skip List", "type": "visualizer", "data_structure": "skip_list", "description": "Skip List Visualizer"},
        {"name": "Unrolled Linked List", "type": "visualizer", "data_structure": "unrolled_linked_list", "description": "Unrolled Linked List Visualizer"},
        {"name": "XOR Linked List", "type": "visualizer", "data_structure": "xor_linked_list", "description": "XOR Linked List Visualizer"},
        
        {"name": "Array", "type": "visualizer", "data_structure": "array", "description": "Basic Array Visualizer"},
        {"name": "Dynamic Array", "type": "visualizer", "data_structure": "dynamic_array", "description": "Dynamic Array (Vector) Visualizer"},
        {"name": "Sparse Array", "type": "visualizer", "data_structure": "sparse_array", "description": "Sparse Array Visualizer"},
        {"name": "Jagged Array", "type": "visualizer", "data_structure": "jagged_array", "description": "Jagged Array Visualizer"},
        {"name": "Circular Array", "type": "visualizer", "data_structure": "circular_array", "description": "Circular Array Buffer Visualizer"},
        
        {"name": "General Tree", "type": "visualizer", "data_structure": "general_tree", "description": "General N-ary Tree"},
        {"name": "Binary Search Tree", "type": "visualizer", "data_structure": "bst", "description": "Interactive BST"},
        {"name": "AVL Tree", "type": "visualizer", "data_structure": "avl_tree", "description": "AVL Tree Self-Balancing"},
        {"name": "Red-Black Tree", "type": "visualizer", "data_structure": "red_black_tree", "description": "Red-Black Tree"},
        {"name": "Splay Tree", "type": "visualizer", "data_structure": "splay_tree", "description": "Splay Tree"},
        {"name": "Treap", "type": "visualizer", "data_structure": "treap", "description": "Treap Random Priority"},
        {"name": "Scapegoat Tree", "type": "visualizer", "data_structure": "scapegoat_tree", "description": "Scapegoat Tree"},
        
        {"name": "B-Tree", "type": "visualizer", "data_structure": "b_tree", "description": "B-Tree Visualizer"},
        {"name": "B+ Tree", "type": "visualizer", "data_structure": "b_plus_tree", "description": "B+ Tree Visualizer"},
        {"name": "B* Tree", "type": "visualizer", "data_structure": "b_star_tree", "description": "B* Tree Visualizer"},
        
        {"name": "Heap", "type": "visualizer", "data_structure": "heap", "description": "Min/Max Heap implementations"},
        {"name": "Fibonacci Heap", "type": "visualizer", "data_structure": "fibonacci_heap", "description": "Fibonacci Heap"},
        {"name": "Binomial Heap", "type": "visualizer", "data_structure": "binomial_heap", "description": "Binomial Heap"},
        {"name": "Pairing Heap", "type": "visualizer", "data_structure": "pairing_heap", "description": "Pairing Heap"},
        
        {"name": "Graph", "type": "visualizer", "data_structure": "graph", "description": "Unified Graph Visualizer (Directed, Undirected, Weighted)"}
    ]
    
    ids = [
        "visualizer_stack",
        "visualizer_queue",
        "visualizer_singly_linked_list",
        "visualizer_doubly_linked_list",
        "visualizer_circular_linked_list",
        "visualizer_circular_doubly_linked_list",
        "visualizer_skip_list",
        "visualizer_unrolled_linked_list",
        "visualizer_xor_linked_list",
        "visualizer_array",
        "visualizer_dynamic_array",
        "visualizer_sparse_array",
        "visualizer_jagged_array",
        "visualizer_circular_array",
        "visualizer_general_tree",
        "visualizer_bst",
        "visualizer_avl",
        "visualizer_rb",
        "visualizer_splay",
        "visualizer_treap",
        "visualizer_scapegoat",
        "visualizer_btree",
        "visualizer_bplus",
        "visualizer_bstar",
        "visualizer_heap",
        "visualizer_fib",
        "visualizer_bin",
        "visualizer_pairing",
        "visualizer_graph"
    ]
    
    # Check if documents already exist
    existing_count = store.count()
    print(f"Current documents in collection: {existing_count}")
    
    # Delete existing documents with the same IDs to avoid duplicate errors
    print("Removing existing documents if they exist...")
    try:
        store.delete(ids=ids)
    except Exception as e:
        print(f"Note: Delete failed (might be first run): {e}")

    # Add documents
    try:
        added_ids = store.add_documents(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"\n✅ Successfully seeded {len(added_ids)} visualizers:")
        for i, doc_id in enumerate(added_ids):
             print(f"   - {metadatas[i]['name']} (ID: {doc_id})")
        
        print(f"\n📊 Total documents in collection: {store.count()}")
        print("\n✨ Seeding completed successfully!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ Error seeding visualizers: {str(e)}")
        raise


if __name__ == "__main__":
    seed_visualizers()
