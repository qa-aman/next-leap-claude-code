# Learning MCP servers

**Sources (read 17-10-2026):**
1. Anthropic, "Introducing the Model Context Protocol", 25-11-2024: https://www.anthropic.com/news/model-context-protocol
2. MCP docs, introduction: https://modelcontextprotocol.io/docs/getting-started/intro
3. MCP docs, architecture: https://modelcontextprotocol.io/docs/learn/architecture
4. MCP docs, server concepts: https://modelcontextprotocol.io/docs/learn/server-concepts
5. MCP specification, latest (version 2026-07-28): https://modelcontextprotocol.io/specification/latest
6. Claude Code docs, MCP: https://code.claude.com/docs/en/mcp

**What this doc is for:** a teach-me session. Each item is ticked only after Aman explains it back, answers a quiz with reasoning, or applies it to a new case.

---

## Checklist

### Stage 1. The problem
- [ ] 1.1 Why a capable model was still not useful enough: "isolation from data"
- [ ] 1.2 Why every new data source was expensive before MCP (one custom integration per pair)
- [ ] 1.3 The options that existed before MCP, and what each cost
- [ ] 1.4 Why a shared protocol fixes it, and the precedent it copied (Language Server Protocol)

### Stage 2. The solution
- [ ] 2.1 Host, client, server: who is who, and why one client per server
- [ ] 2.2 The two layers: data layer (JSON-RPC 2.0) and transport (stdio vs Streamable HTTP)
- [ ] 2.3 The three server primitives and who controls each (tools, resources, prompts)
- [ ] 2.4 Discovery: how a client learns what a server offers (`*/list`, `server/discover`, per-request metadata)
- [ ] 2.5 What a server can ask of the client (elicitation), and what is deprecated (sampling)
- [ ] 2.6 Where the risk sits: approval, trust, prompt injection

### Stage 3. The context
- [ ] 3.1 MCP in Claude Code: `claude mcp add`, the three scopes and which one wins
- [ ] 3.2 Why many servers used to fill the context window, and how tool search fixes it
- [ ] 3.3 When to reach for an MCP server vs a skill, a plugin or a CLI

---

## Stage 1. The problem

*(filled in during the session)*

## Stage 2. The solution

*(filled in during the session)*

## Stage 3. The context

*(filled in during the session)*

---

## Accuracy to-do

| Claim | Status | What would confirm it |
|---|---|---|
| "N apps times M tools" integrations, reduced to N plus M by a standard | Explanation, not a quote. The sources say "every new data source requires its own custom implementation" | It is arithmetic from that sentence, fine to teach as framing |
| Older tutorials show an `initialize` handshake. The 2026-07-28 spec is stateless, with `server/discover` and per-request `_meta` | UNVERIFIED: which spec version changed this | The spec changelog at modelcontextprotocol.io |
