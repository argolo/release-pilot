# 📘 Tutorial — Implementando e Usando o ReleasePilot

## 🎯 Objetivo deste tutorial

Este guia explica como:

* estruturar um projeto compatível com o **ReleasePilot**
* organizar configurações por **contratante** e **ambiente**
* definir comandos `yarn` no padrão esperado
* executar releases de forma **determinística, auditável e controlada**

O foco é **orquestração consciente**, não automação cega.

---

## 🧠 Conceito fundamental

O **ReleasePilot não executa lógica de build**.

Ele **orquestra comandos `yarn` existentes**, seguindo o padrão:

```bash
yarn {platform}:{contractor}:{environment}:{command}
```

Exemplo:

```bash
yarn android:quickup:beta:build
```

Toda a lógica específica (build, assinatura, deploy, upload, etc.) **fica no `package.json` ou em scripts chamados por ele**.
O ReleasePilot apenas **organiza, ordena e executa** esses comandos.

---

## 📦 Passo 1 — Estrutura esperada do projeto

No diretório raiz do projeto, organize os contratantes e ambientes da seguinte forma:

```text
project-root/
├─ contractor/
│  ├─ quickup/
│  │  ├─ sandbox/
│  │  │  └─ config.json
│  │  ├─ beta/
│  │  │  └─ config.json
│  │  └─ prod/
│  │     └─ config.json
│  ├─ kompa/
│  │  ├─ sandbox/
│  │  └─ beta/
│  └─ sp/
│     └─ beta/
├─ package.json
└─ ...
```

### Observações importantes

* As pastas **podem estar vazias**, mas a proposta é que:

  * contenham **arquivos de configuração**
  * armazenem **assets, chaves, manifests ou parâmetros**
* Cada pasta em `contractor/` representa um **contratante**
* Cada subpasta representa um **ambiente**
* A estrutura de diretórios funciona como **fonte de verdade organizacional**

---

## ⚙️ Passo 2 — Definir os scripts no `package.json`

No `package.json`, crie **aliases de scripts** que sigam rigorosamente o padrão do ReleasePilot.

### Exemplo

```json
{
  "scripts": {
    "android:quickup:sandbox:add": "echo 'Preparing Android QuickUp Sandbox'",
    "android:quickup:sandbox:build": "echo 'Building Android QuickUp Sandbox'",
    "android:quickup:sandbox:deploy": "echo 'Deploying Android QuickUp Sandbox'",

    "ios:quickup:sandbox:add": "echo 'Preparing iOS QuickUp Sandbox'",
    "ios:quickup:sandbox:build": "echo 'Building iOS QuickUp Sandbox'",
    "ios:quickup:sandbox:deploy": "echo 'Deploying iOS QuickUp Sandbox'",

    "android:kompa:beta:build": "echo 'Building Android Kompa Beta'",
    "ios:kompa:beta:build": "echo 'Building iOS Kompa Beta'"
  }
}
```

### Boas práticas

* Cada script deve ser **determinístico**
* Evite lógica condicional complexa
* Scripts de baixo nível devem ser chamados **indiretamente**
* O ReleasePilot **não substitui** seus scripts — ele os coordena

---

## 🚀 Passo 3 — Instalar o ReleasePilot

Você pode instalar usando `pip3`:

```bash
pip3 install release-pilot
```

Verifique a instalação:

```bash
release-pilot
```

> ⚠️ O ReleasePilot **não possui `--help`**.
> A interação ocorre diretamente via menu no terminal.

---

## ▶️ Passo 4 — Executar o ReleasePilot

No diretório raiz do projeto:

```bash
release-pilot
```

O menu interativo será exibido automaticamente.

---

## 🧭 Passo 5 — Fluxo de execução interativo

O ReleasePilot solicitará, em ordem:

1. **Platform**

   * `android`
   * `ios`
   * `(all)`

2. **Contractor**

   * Detectado automaticamente a partir de `contractor/`
   * Ou `(all)`

3. **Environment**

   * Detectado por contratante
   * Ou `(all)`

4. **Command**

   * `add`
   * `build`
   * `deploy`
   * Ou `(all)`
     *(executado sempre na ordem correta: add → build → deploy)*

---

## 📌 Passo 6 — Planejamento de execução

Antes da execução, o ReleasePilot apresenta o **plano completo**, exatamente na ordem real:

```text
Execution plan:
yarn android:quickup:beta:add
yarn android:quickup:beta:build
yarn ios:quickup:beta:add
yarn ios:quickup:beta:build
```

Você deve **confirmar explicitamente** antes de continuar.

---

## ⏸️ Passo 7 — Execução assistida (pausas intencionais)

Durante a execução, o ReleasePilot:

* pausa entre **ambientes**
* pausa entre **contratantes**
* aguarda confirmação humana

Exemplo:

```text
Execution paused: Environment 'beta' completed for 'quickup'
Press ENTER to continue...
```

### Por que isso é intencional?

* Recuperar artefatos
* Validar builds
* Sincronizar com pipelines externos
* Reduzir risco em ambientes sensíveis

---

## 📊 Passo 8 — Resumo final do release

Ao final, o ReleasePilot exibe um resumo consolidado:

```text
Release Summary
Project      : RELEASEPILOT
Version      : main
Contractors : quickup, kompa
Environments: beta
Platforms   : android, ios
Commands    : 4
```

E a lista ordenada de comandos executados.

Esse output pode ser usado para:

* auditoria
* registro de release
* comunicação com stakeholders

---

## 🛡️ Boas práticas recomendadas

* ✔️ Use o `contractor/` como organização estrutural
* ✔️ Centralize lógica operacional no `package.json`
* ✔️ Use o ReleasePilot apenas como **orquestrador**
* ✔️ Mantenha checkpoints humanos em produção

---

## 🚫 Anti-patterns (o que evitar)

* ❌ Lógica de build dentro do ReleasePilot
* ❌ Scripts fora do padrão esperado
* ❌ Automatizar produção sem pausas
* ❌ Misturar ambientes ou contratantes
* ❌ Tratar o orquestrador como ferramenta de build

---

## 🏁 Conclusão

O **ReleasePilot** é ideal para equipes que precisam de:

* previsibilidade
* padronização
* controle
* automação consciente

Ele não substitui seus scripts.
Ele **organiza e governa a execução deles**.
