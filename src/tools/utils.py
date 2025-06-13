import os
from langgraph.graph.state import CompiledStateGraph


def visualize_graph(app: CompiledStateGraph):
    """Generate and display the graph visualization."""
    try:
        # Get the graph representation
        graph_image = app.get_graph().draw_mermaid_png()

        # Save the image
        with open(
            os.path.join(os.path.dirname(__file__), "langgraph_visualization.png"), "wb"
        ) as f:
            f.write(graph_image)

        print("✅ Graph visualization saved as 'langgraph_visualization.png'")

        # Also print the mermaid diagram code
        mermaid_code = app.get_graph().draw_mermaid()
        print("\n🎨 Mermaid Diagram Code:")
        print("-" * 50)
        print(mermaid_code)
        print("-" * 50)

        return True
    except Exception as e:
        print(f"❌ Error generating visualization: {e}")
        return False
