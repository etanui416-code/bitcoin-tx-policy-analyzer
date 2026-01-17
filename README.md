# Bitcoin Transaction Policy Analyzer

A Python tool that analyzes Bitcoin transactions from a **mempool policy**
(not consensus) perspective.

## Motivation
Bitcoin Core enforces policy rules that affect transaction relay and mining
without impacting consensus validity. This project models those rules to
support protocol learning and safer contribution.

## What this demonstrates
- Clear separation of policy vs consensus
- Dust output detection
- Fee and feerate analysis
- Standardness checks

## Usage
```bash
python tx_policy_analyzer.py
