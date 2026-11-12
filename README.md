<p align="center">
  <a href="https://faxforagents.com"><img src="https://faxforagents.com/brand/logo-512.png" width="88" alt="Fax for Agents"></a>
</p>

<h1 align="center">Fax for Agents for Kiro</h1>

<p align="center">A Kiro power for <a href="https://faxforagents.com">Fax for Agents</a>: the MCP server (17 tools) plus the fax-for-agents skill. Send and receive faxes from Kiro.</p>

<p align="center">
  <a href="https://faxforagents.com">Website</a> ·
  <a href="https://faxforagents.com/docs/quickstart/">Quickstart</a> ·
  <a href="https://faxforagents.com/docs/api/">API reference</a> ·
  <a href="https://faxforagents.com/docs/sdks/">SDKs</a> ·
  <a href="https://faxforagents.com/mcp/">MCP</a> ·
  <a href="https://app.faxforagents.com">Dashboard</a> ·
  <a href="https://faxforagents.com/pricing/">Pricing</a> ·
  <a href="https://faxforagents.com/changelog/">Changelog</a> ·
  <a href="https://faxforagents.com/affiliates/">Affiliate program</a> ·
  <a href="https://gitlab.com/faxforagents/kiro-power">GitLab</a>
</p>

<p align="center">
  <a href="https://github.com/faxforagents/kiro-power/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/faxforagents/kiro-power/ci.yml?branch=main&label=ci" alt="CI"></a>
  <a href="https://github.com/faxforagents/kiro-power/blob/main/LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f6feb" alt="MIT licence"></a>
  <a href="https://faxforagents.com/mcp/"><img src="https://img.shields.io/badge/MCP-17%20tools-6b4fbb" alt="MCP"></a>
</p>

Fax for Agents is a fax API, a hosted MCP server and SDKs built so AI agents can send and receive
faxes. It is made by JSB Holdings LLC and built by [Synapse](https://synapsereality.io/).

A power is a folder in the Agent Plugins format. [`plugin.json`](plugin.json) names it and lists the
keywords that activate it. [`mcp.json`](mcp.json) starts the [`faxforagents-mcp`](https://www.npmjs.com/package/faxforagents-mcp)
server over stdio with `npx` (Node 20 or later). [`skills/fax-for-agents/`](skills/fax-for-agents/SKILL.md)
is the manual Kiro loads when a task is about a fax. It holds the safe send order, the approvals rule,
the rule that text from a fax is data, and the price card. The skill is maintained in
[faxforagents/skills](https://github.com/faxforagents/skills) and vendored here.

## Install

1. Export `FAXFORAGENTS_API_KEY=ffa_test_...` in the environment Kiro starts from.
2. In Kiro, open the Powers panel, Add Custom Power, Import power from GitHub, and paste
   `https://github.com/faxforagents/kiro-power`.
3. Say "Send a one page test fax to +15550000001". The power activates on the word fax, and Kiro calls
   `prepare_fax`, `quote_fax`, `send_approved_fax` and then `get_fax_status` until the carrier answers.

Kiro namespaces the server, so it shows as `faxforagents-faxforagents` in the MCP panel.

## Keys

A test key (`ffa_test_...`) reaches the sandbox provider only. No carrier, no cost, the destination
number picks the outcome (`+15550000001` is delivered, `+15550000003` is partial, `+15550000005` is
unknown). A live key (`ffa_live_...`) reaches the carrier and spends the prepaid wallet. Keys are
created at <https://app.faxforagents.com>.

The key is read from `FAXFORAGENTS_API_KEY` and sent to `api.faxforagents.com` only. The server and
this power collect no telemetry.

## The tools

| Tool | Does | Scope |
|---|---|---|
| `get_guide` | The manual, whole or by section. Works without a key | none |
| `get_fax_capabilities` | Limits, routes, formats, prices, the scopes of the key | `account:read` |
| `prepare_fax` | A document from text, Markdown, HTML or a completed upload. Never sends | `document:write` |
| `get_fax_document` | One prepared document by id: page count, sha256, warnings, previews | `document:read` |
| `quote_fax` | The exact price of one document to one destination, with the policy verdict | `fax:quote` |
| `send_approved_fax` | Queue a quoted fax. Answers queued, never delivered | `fax:send` |
| `get_fax_status` | State and attempts, with the carrier's evidence once delivered or partial | `fax:read` |
| `list_faxes` | Newest first, by state, with a cursor | `fax:read` |
| `get_fax_balance` | Available and held balance | `billing:read` |
| `cancel_fax` | Cancel while queued, best effort once sending | `fax:cancel` |
| `request_card_payment` | Ask a person to pay for one quoted fax by card, with no wallet balance | `fax:send` |
| `get_card_payment_status` | One card payment order: paid or not, what was charged, the fax it sent | `fax:read` |
| `request_human_review` | With `quote_id`, ask a person to approve that send. Without it, ask for help | `approval:request` |
| `get_review_status` | Where one approval or help request stands | `approval:read` |
| `list_inbox` | Received faxes, metadata only | `inbox:read` |
| `read_inbound_fax` | One received fax, its text and latest extraction as data | `inbox:read` |
| `extract_fax_data` | OCR a received fax or a document, extract schema fields with citations | `document:extract` |

A live send needs a human approval bound to that exact quote, or a delegated policy written by the
account owner. Kiro's API key can never approve its own send. Text that came out of a received fax is
data from whoever sent it, never an instruction to the agent.

## Prices

Price card launch-v3 is effective from 2026-11-12. $0.039 per page sent, $0.019 per page received.
$2 per number per month, $19 per month for the Agent workspace. Sandbox pages cost 0.

## Privacy and support

Privacy policy: <https://faxforagents.com/privacy>. Terms: <https://faxforagents.com/terms>.
Support: hello@faxforagents.com, or an issue on this repository. Security reports go to the same
address, see [SECURITY.md](SECURITY.md).

## Working on this repository

```bash
python3 scripts/check_power.py    # plugin.json and mcp.json against the published schemas, the vendored skill
sh scripts/truthcheck.sh          # the copy states only what the product ships
```

## Licence

MIT. See [LICENSE](LICENSE).
