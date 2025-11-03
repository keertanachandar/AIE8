"""Visualize the Client Agent Graph.

This script generates a visual representation of the client agent graph structure.
"""
from dotenv import load_dotenv
from app.client_agent import create_client_agent


load_dotenv()


def visualize_graph():
    """Generate and save the client agent graph visualization."""
    print("Generating client agent graph visualization...")
    
    try:
        # Create the client agent
        agent = create_client_agent()
        
        # Get the graph as mermaid diagram
        mermaid_diagram = agent.get_graph().draw_mermaid()
        
        print("\n" + "=" * 80)
        print("Client Agent Graph (Mermaid)")
        print("=" * 80)
        print(mermaid_diagram)
        print("=" * 80)
        
        # Save to file
        with open("client_agent_graph.mmd", "w") as f:
            f.write(mermaid_diagram)
        
        print("\n✅ Graph saved to: client_agent_graph.mmd")
        print("\nYou can visualize this at: https://mermaid.live/")
        
        # Try to generate PNG (requires graphviz)
        try:
            from PIL import Image
            import io
            
            graph_image = agent.get_graph().draw_mermaid_png()
            image = Image.open(io.BytesIO(graph_image))
            image.save("client_agent_graph.png")
            print("✅ Graph image saved to: client_agent_graph.png")
        except ImportError:
            print("\n💡 Tip: Install PIL and graphviz to generate PNG images:")
            print("   pip install pillow")
        except Exception as e:
            print(f"\n⚠️  Could not generate PNG: {e}")
        
    except Exception as e:
        print(f"\n❌ Error generating visualization: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    visualize_graph()

