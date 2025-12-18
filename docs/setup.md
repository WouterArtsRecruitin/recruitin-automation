# Setup Guide

## Vereisten

- Python 3.10+
- HuggingFace account (gratis)

## 1. Clone Repository

```bash
git clone git@github.com:WouterArtsRecruitin/recruitin-automation.git
cd recruitin-automation
```

## 2. Installeer Dependencies

```bash
pip install -r requirements.txt
```

## 3. HuggingFace Token

1. Ga naar https://huggingface.co/settings/tokens
2. Maak een token aan (Read access)
3. Export als environment variable:

```bash
export HF_TOKEN="hf_xxxxx"
```

## 4. Claude Desktop Configuratie

Voeg toe aan `~/.config/claude/claude_desktop_config.json` (Linux) of `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "cv_parser": {
      "command": "python",
      "args": ["/pad/naar/recruitin-automation/mcp-servers/cv-parser/server.py"],
      "env": {
        "HF_TOKEN": "hf_xxxxx"
      }
    }
  }
}
```

## 5. Test

```bash
cd mcp-servers/cv-parser
python server.py
```

## Data Bestanden

- **JobDigger export:** Excel met vacatures (Vacature, Bedrijfsnaam, Plaats)
- **CV's:** PDF bestanden, text wordt automatisch geëxtraheerd

## Workflow

1. Upload JobDigger Excel → wordt geconverteerd naar vacatures lijst
2. Upload CV PDF → tekst extractie
3. `parse_cv` → kandidaat profiel
4. `match_cv_to_vacancies` → TIER1/2/3 matches
5. `semantic_match` → finetuning similarity scores
