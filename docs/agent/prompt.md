# Prompt

> Estrutura conforme `../standards/prompt_standard.md`. Este documento descreve a composição do prompt de sistema; o texto literal enviado ao LLM é implementação e deve apenas referenciar, não duplicar, o conteúdo dos documentos abaixo.

## Composição do prompt de sistema

1. **Papel/persona** — derivado integralmente de `persona.md` (consultivo, técnico, direto, honesto sobre incerteza).
2. **Objetivo da tarefa** — derivado de `objectives.md`, específico a cada skill (identificar padrão, gerar NFRs, gerar ADRs, etc. — ver `agent_design.md`).
3. **Instruções de comportamento** — derivadas de `ai_spec.md` (comportamento em caminho feliz, fonte ambígua e fora de escopo).
4. **Regras/guardrails reforçados** — RULE-SA-1 a RULE-SA-9 (`rules.md`) e os guardrails GR-SA-1 a GR-SA-8 (`guardrails.md`) devem aparecer de forma explícita e não negociável no prompt, não apenas implícita no tom. Em particular, `identify_architecture_pattern` sempre lista o catálogo fechado de padrões no próprio prompt (GR-SA-1).
5. **Formato de saída** — schema de `output_schema.md`, incluindo os valores válidos de `status`.
6. **Exemplos (few-shot)** — extraídos de `knowledge/examples/` quando existir (ainda não criado nesta fase); ausência de exemplos não deve degradar o comportamento esperado, apenas reduzir a calibração fina de estilo.

## Convenções de versionamento

- Cada versão do prompt é identificada, permitindo associar uma versão a um conjunto de resultados de `evaluation.md`.
- Mudanças que alterem comportamento observável (não apenas fraseado) exigem rodar os casos de teste de `evaluation.md` antes de substituir a versão em uso.

## O que o prompt não deve conter

- Não deve conter conhecimento de domínio específico de cliente diretamente embutido.
- Não deve reafirmar informações já garantidas estruturalmente pelo schema de saída.
- Não deve listar tecnologias/produtos específicos fora do catálogo de padrões arquiteturais — isso pertenceria a uma fase futura, quando existir uma fonte de "padrões tecnológicos da organização" (GR-SA-5).
