#!/bin/bash
# =============================================================
# overnight-ortofoto.sh
# Script para rodar Ralph Wiggum overnight no pipeline de ortofoto
# 
# USO:
#   chmod +x overnight-ortofoto.sh
#   ./overnight-ortofoto.sh
#
# PRÉ-REQUISITOS:
#   1. Claude Code instalado e autenticado
#   2. Plugin Ralph Wiggum instalado:
#      /plugin install ralph-loop@claude-plugins-official
#   3. PROMPT_RALPH_WIGGUM.md na raiz do projeto
# =============================================================

echo "🚀 Ortofoto Pipeline — Ralph Wiggum Overnight Run"
echo "================================================="
echo "Início: $(date)"
echo ""

PROJECT_ROOT="$(pwd)"
PROMPT_FILE="$PROJECT_ROOT/PROMPT_RALPH_WIGGUM.md"
MAX_ITERATIONS=50
COMPLETION_PROMISE="PIPELINE_COMPLETE"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "❌ PROMPT_RALPH_WIGGUM.md não encontrado em $PROJECT_ROOT"
    exit 1
fi

echo "📄 Prompt: $PROMPT_FILE"
echo "🔄 Max iterações: $MAX_ITERATIONS"
echo "🏁 Completion: $COMPLETION_PROMISE"
echo ""
echo "Iniciando em 5s... (Ctrl+C para cancelar)"
sleep 5

# ---- OPÇÃO 1: Plugin Ralph Wiggum ----
PROMPT_CONTENT=$(cat "$PROMPT_FILE")
/ralph-loop:ralph-loop "$PROMPT_CONTENT" \
    --max-iterations $MAX_ITERATIONS \
    --completion-promise "$COMPLETION_PROMISE"

# ---- OPÇÃO 2: Loop Bash Puro (descomente se preferir) ----
# ITERATION=0
# while [ $ITERATION -lt $MAX_ITERATIONS ]; do
#     ITERATION=$((ITERATION + 1))
#     echo ""
#     echo "=== Iteração $ITERATION / $MAX_ITERATIONS — $(date) ==="
#     OUTPUT=$(cat "$PROMPT_FILE" | claude 2>&1)
#     echo "$OUTPUT"
#     if echo "$OUTPUT" | grep -q "$COMPLETION_PROMISE"; then
#         echo "✅ COMPLETO na iteração $ITERATION!"
#         exit 0
#     fi
#     sleep 2
# done
# echo "⚠️ Max iterações atingido."

echo "🏁 Fim: $(date)"
