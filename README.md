# Recruitin Automation Hub

🚀 **MCP Servers, Workflows & Tools voor AI-powered Recruitment**

Recruitin B.V. | December 2024

---

## 📦 Inhoud

```
recruitin-automation/
├── mcp-servers/
│   └── cv-parser/          # CV parsing & matching
├── workflows/
│   └── candidate-matching/ # Kandidaat → Vacature matching
├── scripts/
│   └── cv_parser.py        # Standalone CV parser
└── docs/
    └── setup.md            # Installatie instructies
```

---

## 🔧 MCP Servers

### CV Parser MCP
Parse CVs en match tegen vacatures.

```bash
cd mcp-servers/cv-parser
pip install -r requirements.txt
python server.py
```

**Tools:**
| Tool | Functie |
|------|---------|
| `parse_cv` | CV tekst → kandidaat profiel |
| `match_cv_to_vacancies` | CV + vacatures → ranked matches |
| `semantic_match` | HuggingFace similarity |
| `extract_skills` | Skill analyse |

---

## ⚡ Quick Start

```bash
git clone git@github.com:WouterArtsRecruitin/recruitin-automation.git
cd recruitin-automation
pip install -r requirements.txt
```

### Claude Desktop Config

```json
{
  "mcpServers": {
    "cv-parser": {
      "command": "python",
      "args": ["./mcp-servers/cv-parser/server.py"],
      "env": {
        "HF_TOKEN": "hf_xxxxx"
      }
    }
  }
}
```

---

## 📊 Response Rates

| Methode | Response Rate |
|---------|---------------|
| Generic outreach | 15-20% |
| **Met dit systeem** | **50-60%** |

---

## 📝 License

Proprietary - Recruitin B.V.

**Contact:** warts@recruitin.nl
