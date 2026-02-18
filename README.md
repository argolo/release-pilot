# 🚀 ReleasePilot

**ReleasePilot** é um **orquestrador assistido de releases** que executa comandos `yarn` de forma **organizada, determinística e controlada**, a partir de variáveis informadas pelo operador (plataforma, contratante, ambiente e comando).

Seu objetivo é **automatizar e padronizar o processo de construção, empacotamento e entrega de aplicativos white-label**, respeitando as particularidades de cada contratante, ambiente e plataforma, sem abrir mão do **controle humano em pontos críticos**.

---

## 🎯 Propósito

O ReleasePilot foi criado para resolver um problema recorrente em ecossistemas white-label:

> **Como executar múltiplos comandos de build de forma consistente, previsível e auditável, quando cada aplicação possui variações por contratante, ambiente e plataforma?**

A resposta não é automação cega — é **orquestração consciente**.

---

## ✨ Principais Características

* 🎛️ Orquestração de comandos `yarn` baseada em variáveis operacionais
* 📱 Suporte a múltiplas plataformas (`android`, `ios`)
* 🏢 Descoberta automática de **contratantes** via estrutura de diretórios
* 🧪 Descoberta automática de **ambientes** por contratante
* ⚙️ Comandos suportados: `add`, `build`, `deploy`
* 🔁 Opção **“todas”** em todas as seleções
* ⏸️ Execução **assistida**, com pausas humanas entre:

  * Ambientes
  * Contratantes
* 📌 Planejamento de execução **idêntico à ordem real**
* 📦 Resumo final rastreável do release
* 🧩 Código simples, pythonico e sem dependências externas

---

## 🧠 Filosofia de Operação

O ReleasePilot **não executa comandos aleatoriamente**.

Ele:

* Organiza
* Ordena
* Opera

Cada comando `yarn` é executado dentro de um **contexto bem definido**, garantindo que:

* Builds não se misturem entre contratantes
* Ambientes sejam respeitados
* Artefatos possam ser recuperados entre etapas
* O operador tenha clareza total do que está sendo executado

---

## 📂 Estrutura Esperada do Projeto

```text
project-root/
├─ contractor/
  ├─ quickup/
  │  ├─ sandbox/
  │  └─ beta/
  |  └─ alfa/
  ├─ kompa/
     ├─ sandbox/
     └─ beta/
     └─ prod/

```

> O nome do projeto é automaticamente inferido a partir do **diretório raiz**.

---

## 🧾 Padrão de Comando Executado

O ReleasePilot executa comandos no seguinte formato:

```bash
yarn {plataforma}:{contratante}:{ambiente}:{comando}
```

### Exemplo

```bash
yarn android:quickup:beta:build
```

---

## 🚀 Instalação

### Requisitos

* Python **3.9+**
* Node.js + Yarn
* Git (opcional, mas recomendado para rastreabilidade)

### Instalação local (desenvolvimento)

```bash
pip install -e .
```

### Instalação padrão

```bash
pip install .
```

Após a instalação, o comando estará disponível como:

```bash
release-pilot
```

---

## ▶️ Uso

Execute o comando no diretório raiz do projeto:

```bash
release-pilot
```

O ReleasePilot irá solicitar, de forma interativa:

1. Plataforma
2. Contratante
3. Ambiente
4. Comando

Em todas as etapas é possível selecionar **uma opção específica** ou **todas**, permitindo execução combinatória controlada.

---

## ⏸️ Execução Assistida

Durante a execução, o ReleasePilot **pausa automaticamente** entre ambientes e contratantes, aguardando confirmação explícita do operador.

Esse comportamento é intencional e garante:

* Recuperação de artefatos
* Validação manual
* Sincronização com pipelines externos
* Redução de risco em produção

---

## 📌 Planejamento de Execução

Antes de executar qualquer comando, o ReleasePilot exibe o **planejamento completo**, exatamente na **ordem em que os comandos serão executados**.

Isso elimina ambiguidades e garante previsibilidade total.

---

## ✅ Resumo Final de Release

Ao final da execução, o ReleasePilot apresenta um resumo consolidado contendo:

* 📁 Projeto
* 📦 Contratantes
* 🌿 Versão
* 🧪 Ambientes
* 📱 Plataformas
* ⚙️ Total de comandos executados

Esse resumo facilita auditoria, comunicação e rastreabilidade do release.

---

## 🛡️ Casos de Uso Ideais

* Construção de apps white-label
* Ambientes sandbox / alfa / beta / produção
* Equipes com múltiplos clientes
* Releases sensíveis ou regulados
* Times que precisam de **controle + automação**

---

## 🔮 Evoluções Futuras

* Modo `--dry-run`
* Execução não interativa (`--ci`)
* Exportação de resumo (`.txt` / `.md`)
* Inclusão de commit hash e tag SemVer
* Integração com Slack / Jira / Discord / Telegran
* Persistência de logs

---

## 📜 Licença

MIT License.

---

## 👤 Autor

Desenvolvido por **André Argôlo**
CTO • Arquiteto de Software • DevOps
