---
name: connect-mcp
description: Installer un serveur MCP au niveau utilisateur (Claude Code, Claude Desktop, OpenCode). Utiliser pour "ajouter un MCP", "installer un MCP", "connecter un outil IA externe", "donner acces a X a mon IA".
user-invocable: true
context: main
argument-hint: <nom ou description du MCP>
---

# /connect-mcp : installer un serveur MCP

`$ARGUMENTS` = nom ou description du MCP a installer (ex : "firecrawl", "notion", "supabase", "playwright"). Si vide, demande lequel.

Cible **Claude Code** en priorite, puis Claude Desktop et OpenCode s'ils sont detectes.

## 1. Identifier le MCP
Ne suppose rien, cherche (recherche web) :
1. `"<nom> MCP npm package site:npmjs.com OR site:github.com"`
2. Recupere le README pour la config exacte
3. Verifie dans `https://github.com/modelcontextprotocol/servers` si officiel

Extrais : nom canonique, package npm exact, transport (`local`/stdio le plus courant, ou `remote` HTTP/SSE), variables d'environnement requises (+ ou les obtenir), args speciaux.

## 2. Detecter les outils installes
```bash
echo "=== Detection outils IA ==="
[ -f "$HOME/.claude.json" ] && echo "Claude Code CLI: DETECTE" || echo "Claude Code CLI: absent"
[ -f "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ] && echo "Claude Desktop: DETECTE" || echo "Claude Desktop: absent"
[ -f "$HOME/.config/opencode/opencode.json" ] && echo "OpenCode: DETECTE" || echo "OpenCode: absent"
command -v jq >/dev/null && echo "jq: dispo" || echo "jq: ABSENT (fallback Python)"
```

## 3. Demander les cles si necessaire
Si le MCP requiert des variables d'environnement, indique lesquelles et ou les obtenir, et demande les valeurs avant d'ecrire la config. Ne pas continuer sans elles si obligatoires.

## 4. Patcher les configs (ne jamais ecraser l'existant)

### Claude Code CLI (prioritaire)
Methode CLI propre :
```bash
claude mcp add --transport stdio --scope user --env CLE=VALEUR NOM -- npx -y PACKAGE
```
Fallback jq sur `~/.claude.json` (format : `command: "npx"`, `args: [...]`, `env: {}`) :
```bash
[ -f "$HOME/.claude.json" ] || echo '{"mcpServers":{}}' > "$HOME/.claude.json"
jq '.mcpServers["NOM"] = {"command":"npx","args":["-y","PACKAGE"],"env":{"CLE":"VALEUR"}}' \
  "$HOME/.claude.json" > /tmp/cc.json && mv /tmp/cc.json "$HOME/.claude.json"
```

### Claude Desktop (si detecte)
Meme format `mcpServers`. Path macOS : `~/Library/Application Support/Claude/claude_desktop_config.json`. Patcher avec jq comme ci-dessus. Redemarrage de l'app requis.

### OpenCode (si detecte)
`~/.config/opencode/opencode.json`. Format different : `command` est un tableau, variables sous `environment`, `type: "local"`, `enabled: true`.
```bash
jq '.mcp["NOM"] = {"type":"local","command":["npx","-y","PACKAGE"],"environment":{"CLE":"VALEUR"},"enabled":true}' \
  "$HOME/.config/opencode/opencode.json" > /tmp/oc.json && mv /tmp/oc.json "$HOME/.config/opencode/opencode.json"
```

Fallback Python si jq absent (lire le JSON, ajouter la cle, reecrire avec indent=2).

## 5. Verifier
- Claude Code : `claude mcp list` (le MCP apparait)
- OpenCode : `/mcp` dans le chat
- Claude Desktop : redemarrer, verifier les outils dispo
- Test fonctionnel simple si possible (ex : un scrape pour un MCP de scraping)

## 6. Recap
```
MCP installe : <nom> (<package>)
Configure sur : Claude Code [oui/non], Claude Desktop [oui+redemarrage/non], OpenCode [oui/non]
Variables : [definies]
Verifier : claude mcp list
```

## Notes techniques
- MCP sans variable : omettre le bloc env/environment (pas d'objet vide).
- Args supplementaires (ex `--headless`) : apres le package dans args.
- MCP remote : `type: "sse"` + `url` au lieu de command/args (verifier le README).
- npx absent : proposer d'installer Node (`brew install node`).
- Format Claude Code/Desktop (`command` string + `args`) different d'OpenCode (`command` tableau + `environment`). Ne pas confondre : source d'erreur la plus frequente.
- Francais, vouvoiement, pas d'em-dash ni en-dash.
