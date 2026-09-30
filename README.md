# Penetration Testing Atlas

An independent bilingual learning site for systems and security engineers. Default English, with Chinese available on every page.

**Published site:** https://shundazhang.github.io/penetration-testing/

16 chapters cover foundations and theory, testing methodology, Web/API, networks and wireless, identity/AD and human workflows, cloud/Kubernetes, hosts/native code, mobile, IoT/OT, tools, AI-assisted testing, AI system security, reporting, exercises and sources.

14 original semantic HTML figures illustrate trust boundaries, test loops, control paths, cloud policy, device lifecycle, AI authority and evidence. The searchable tool shelf explains 28 tools with official documentation and interpretation limits. The primary-source catalog contains 57 references, including published standards, versioned OWASP guides, platform documentation, author repositories and research papers.

## Build and preview

Requires Python 3; no third-party build dependencies.

```sh
python3 -B build.py
python3 -m http.server 8768 --bind 127.0.0.1
```

Open http://localhost:8768/ . GitHub Pages serves generated files from the main branch root.

Edit `content.py` for bilingual notes, the tool catalog and sources; `diagrams.py` for figures; `build.py` for layouts; `labs.js` for local exercises; and `tools.js` for filtering. Generated HTML is committed for static hosting.

## Exercises and scope

Four deterministic browser exercises illustrate an authorization matrix, evidence interpretation, a coverage ledger and an agent capability boundary. They use synthetic fixtures, make no target requests, invoke no tools or models, and store no user input. They are teaching simulations, not a backend access-control library or an AI attack benchmark. `labs/assessment-template.md` is a bilingual downloadable notebook for scoped training assessments and retests.

The site provides study material for authorized testing. It does not operate scanners against visitors or external targets. No third-party scripts, fonts, analytics, authentication or model services are required.

## Source status

Reviewed on 30 September 2026. WSTG references released v4.2; ASVS references 5.0.0. Awareness sources include Web Top 10:2025, API Top 10:2023, LLM Top 10:2026 and Agentic Top 10:2026. MCP authorization is linked to the 2026-07-28 version. Historical methodology, living documentation and research are labeled separately. Tool versions, platform behavior, errata and project status should be checked in the linked primary sources.

Explanations, fixtures, layouts and figures are original study material. Referenced specifications and tools retain their respective authorship and licensing. No third-party logos or diagrams are redistributed.
