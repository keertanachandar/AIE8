<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

## <h1 align="center" id="heading">Session 15: Build & Serve an A2A Endpoint for Our LangGraph Agent</h1>

| 🤓 Pre-work | 📰 Session Sheet | ⏺️ Recording     | 🖼️ Slides        | 👨‍💻 Repo         | 📝 Homework      | 📁 Feedback       |
|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|:-----------------|

# A2A Protocol Implementation with LangGraph

This session focuses on implementing the **A2A (Agent-to-Agent) Protocol** using LangGraph, featuring intelligent helpfulness evaluation and multi-turn conversation capabilities.

## 🎯 Learning Objectives

By the end of this session, you'll understand:

- **🔄 A2A Protocol**: How agents communicate and evaluate response quality

## 🎉 Project Status

### ✅ Activity #1 Complete: A2A Client Agent Built!

A complete **LangGraph-based client agent** has been implemented that demonstrates agent-to-agent communication through the A2A protocol.

**📦 What's Included:**
- 🔧 **A2A Tool Layer** - LangChain tools that wrap A2A API calls
- 🤖 **Client Agent Graph** - Intelligent agent that delegates to the server
- 💻 **Interactive CLI** - User-friendly interface for testing
- ✅ **Automated Tests** - Complete test suite (all passing)
- 📚 **Comprehensive Docs** - Architecture, guides, and examples

**🚀 Quick Links:**
- 📘 [Quick Start Guide](./QUICKSTART_CLIENT.md) - Get started in 5 minutes
- 📖 [Technical Documentation](./CLIENT_AGENT.md) - Complete implementation guide
- 🏗️ [Architecture Overview](./ARCHITECTURE.md) - System design and flow
- ✅ [Solution Summary](./ACTIVITY_1_SOLUTION.md) - What was built

**🎯 Try It Now:**
```bash
# Terminal 1: Start the A2A server
uv run python -m app

# Terminal 2: Run the client agent
uv run python app/run_client_agent.py -i
```

---

## 🧠 A2A Protocol with Helpfulness Loop

The core learning focus is this intelligent evaluation cycle:

```mermaid
graph TD
    A["👤 User Query"] --> B["🤖 Agent Node<br/>(LLM + Tools)"]
    B --> C{"🔍 Tool Calls<br/>Needed?"}
    C -->|"Yes"| D["⚡ Action Node<br/>(Tool Execution)"]
    C -->|"No"| E["🎯 Helpfulness Node<br/>(A2A Evaluation)"]
    D --> F["🔧 Execute Tools"]
    F --> G["📊 Tavily Search<br/>(Web Results)"]
    F --> H["📚 ArXiv Search<br/>(Academic Papers)"]  
    F --> I["📄 RAG Retrieval<br/>(Document Search)"]
    G --> B
    H --> B
    I --> B
    E --> J{"✅ Is Response<br/>Helpful?"}
    J -->|"Yes (Y)"| K["🏁 END<br/>(Task Complete)"]
    J -->|"No (N)"| L{"🔄 Loop Count<br/>< 10?"}
    L -->|"Yes"| B
    L -->|"No"| K
    
    style A fill:#1e3a5f,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style B fill:#4a148c,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style C fill:#0d47a1,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style D fill:#1b5e20,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style E fill:#e65100,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style F fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style G fill:#00695c,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style H fill:#4527a0,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style I fill:#283593,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style J fill:#2e7d32,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style K fill:#c62828,stroke:#ffffff,stroke-width:3px,color:#ffffff
    style L fill:#f57c00,stroke:#ffffff,stroke-width:3px,color:#ffffff
```

# Build 🏗️

Complete the following tasks to understand A2A protocol implementation:

## 🚀 Quick Start

```bash
# Setup and run
./quickstart.sh
```

```bash
# Start LangGraph server
uv run python -m app
```

```bash
# Test the A2A Serer
uv run python app/test_client.py
```

### 🏗️ Activity #1:

Build a LangGraph Graph to "use" your application.

Do this by creating a Simple Agent that can make API calls to the 🤖Agent Node above through the A2A protocol. 

#### ✅ **COMPLETED - A2A Client Agent Built!**

A complete LangGraph client agent has been implemented that communicates with the A2A server.

**🚀 Quick Start - Client Agent:**

```bash
# Start the A2A server first (in one terminal)
uv run python -m app

# Run the interactive client agent (in another terminal)
uv run python app/run_client_agent.py -i

# Or run a single query
uv run python app/run_client_agent.py -q "What are the latest AI developments?"
```

**📁 Files Created:**
- `app/a2a_tool.py` - LangChain tool for A2A API calls
- `app/client_agent.py` - LangGraph client agent implementation  
- `app/run_client_agent.py` - Interactive CLI runner
- `app/visualize_client.py` - Graph visualization
- `CLIENT_AGENT.md` - Complete documentation

**📚 Full Documentation:**
See [CLIENT_AGENT.md](./CLIENT_AGENT.md) for detailed architecture, usage examples, and customization guide.

**🎯 What It Does:**
The client agent intelligently delegates tasks to your A2A server agent when it needs:
- Real-time web search (via Tavily)
- Academic paper search (via ArXiv)  
- Document retrieval (via RAG)

For simple queries, it responds directly without calling the A2A server.

### ❓ Question #1:

What are the core components of an `AgentCard`?

##### ✅ Answer:

An `AgentCard` contains:
1. Identity - `name`, `description`, `version`, `url`
2. Protocol - `protocolVersion`, `preferredTransport` (e.g., "JSONRPC")
3. Capabilities - `streaming`, `pushNotifications` (boolean flags)
4. Skills - Array of skills with `id`, `name`, `description`, `tags`, and `examples`
5. I/O Modes - `defaultInputModes`, `defaultOutputModes` (supported content types)

It's essentially a discovery document that advertises what an agent can do and how to communicate with it, similar to an OpenAPI spec for agents.

### ❓ Question #2:

Why is A2A (and other such protocols) important in your own words?

##### ✅ Answer:

A2A is important because it lets diffferent AI systems communicate and collaborate directly, without manual or human mediation between each step.
As AI gets more complex, one system can't be an expert at everything - being able to let different AIs work together, which each can have a specific expertise, creates more powerful and all emcompassing tools.
For example - you might need to analyze specific data/metrics and then create a presentation based on the findings. You'd have one agent to do the data analysis. Without A2A, i'd manually create charts based on the results and then paste those into a deck. With A2A, after the data results are done, it would call the visualization agent that would create the charts for me, and then the presentation agent which would create the slides with the charts and findings.
They could all use different models or be from different companies, but together they help with one larger action item.

<br /><br />

<details>
<summary>🚧 Advanced Build 🚧 (OPTIONAL - <i>open this section for the requirements</i>)</summary>

Use a different Agent Framework to **test** your application.

Do this by creating a Simple Agent that acts as different personas with different goals and have that Agent use your Agent through A2A. 

Example:

"You are an expert in Machine Learning, and you want to learn about what makes Kimi K2 so incredible. You are not satisfied with surface level answers, and you wish to have sources you can read to verify information."
</details>

## 📁 Implementation Details

For detailed technical documentation, file structure, and implementation guides, see:

**➡️ [app/README.md](./app/README.md)**

This contains:
- Complete file structure breakdown
- Technical implementation details
- Tool configuration guides
- Troubleshooting instructions
- Advanced customization options

# Ship 🚢

- Short demo showing running Client

# Share 🚀

- Explain the A2A protocol implementation
- Share 3 lessons learned about agent evaluation
- Discuss 3 lessons not learned (areas for improvement)

# Submitting Your Homework

## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:
1. Create a branch of your `AIE8` repo to track your changes. Example command: `git checkout -b s15-assignment`
2. Complete the activity above
3. Answer the questions above _in-line in this README.md file_
4. Record a Loom video reviewing the Simple Agent you built for Activity #1 and the results.
5. Commit, and push your changes to your `origin` repository. _NOTE: Do not merge it into your main branch._
6. Make sure to include all of the following on your Homework Submission Form:
    + The GitHub URL to the `15_A2A_LANGGRAPH` folder _on your assignment branch (not main)_
    + The URL to your Loom Video
    + Your Three Lessons Learned/Not Yet Learned
    + The URLs to any social media posts (LinkedIn, X, Discord, etc.) ⬅️ _easy Extra Credit points!_

### OPTIONAL: 🚧 Advanced Build Assignment 🚧
<details>
  <summary>(<i>Open this section for the submission instructions.</i>)</summary>

Follow these steps to prepare and submit your homework assignment:
1. Create a branch of your `AIE8` repo to track your changes. Example command: `git checkout -b s015-assignment`
2. Complete the requirements for the Advanced Build
3. Record a Loom video reviewing the agent you built and demostrating in action
4. Commit, and push your changes to your `origin` repository. _NOTE: Do not merge it into your main branch._
5. Make sure to include all of the following on your Homework Submission Form:
    + The GitHub URL to the `15_A2A_LANGGRAPH` folder _on your assignment branch (not main)_
    + The URL to your Loom Video
    + Your Three Lessons Learned/Not Yet Learned
    + The URLs to any social media posts (LinkedIn, X, Discord, etc.) ⬅️ _easy Extra Credit points!_
</details>