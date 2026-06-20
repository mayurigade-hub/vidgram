# VidGram Backend 2 (Risk & Financial Engine) – Master Documentation

## Project Overview

**What the project does:**
Backend 2 is a TypeScript-based orchestration and financial risk engine. It consumes the raw authenticity scores from Backend 1 and translates them into hard financial metrics. It calculates how fake followers directly translate to wasted budget, evaluates the true cost per genuine follower, and compares multiple influencers to recommend the safest financial investment.

**Problem being solved:**
Knowing an influencer has "30% fake followers" is not enough for marketing decisions. Brands need to know exactly how much money that 30% equates to. This system converts abstract fraud probabilities into concrete dollar amounts and actionable business logic.

**High-level workflow:**
Receive influencer profile + Backend 1 risk score → Calculate genuine reach → Compute financial budget loss → Compare against alternatives → Output standardized financial risk metrics.

---

## System Architecture

The architecture relies on strongly typed interfaces and isolated calculation modules to ensure financial formulas are independently testable.

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend API Consumer                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Orchestration Service                        │
│  (src/examples/usage.ts acting as the main entrypoint)         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
┌───────▼────────────┐            ┌──────────▼────────────┐
│ Risk & Analytics   │            │ Financial Formulas    │
│ (riskService.ts)   │            │ (formulas.ts)         │
│                    │            │                       │
│ ├─ Classify Risk   │            │ ├─ Genuine Reach Calc │
│ ├─ Risk Metrics    │            │ ├─ Fake Reach Calc    │
│ └─ Integration     │            │ ├─ Budget Loss Calc   │
│                    │            │ └─ True Cost Per User │
└───────┬────────────┘            └──────────┬────────────┘
        │                                    │
┌───────▼────────────────────────────────────▼────────────────────┐
│                    Comparison Engine                            │
│                  (comparisonService.ts)                         │
│  - Evaluates Influencer A vs. Influencer B                     │
│  - Determines "Safer Choice" and "Potential Savings"           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```text
backend2/risk-engine/
├── package.json              # Dependencies (TypeScript, ts-node)
├── tsconfig.json             # Compiler configuration (CommonJS)
└── src/
    ├── types/
    │   └── index.ts          # Centralized interface definitions
    ├── utils/
    │   └── formulas.ts       # Pure mathematical functions
    ├── services/
    │   ├── riskService.ts    # Service to aggregate single influencer risk
    │   └── comparisonService.ts # Service to compare multiple influencers
    └── examples/
        └── usage.ts          # Executable orchestration script
```

### Folder Purposes
- **types/**: Enforces the input/output contracts (e.g., `RiskMetrics`, `InfluencerInput`).
- **utils/**: Pure functions for math calculations, ensuring they can be unit-tested without mock dependencies.
- **services/**: The core business logic that glues data and formulas together.
- **examples/**: Demonstration scripts acting as the temporary API controller.

---

## Data Flow

### End-to-End Example: Financial Risk Calculation

**Step 1: Input Payload**
```typescript
const influencer = {
  followers: 100000,
  authenticityScore: 80
};
const context = { campaignBudget: 250000 };
```

**Step 2: Utility Calculations (`formulas.ts`)**
- `genuineReach`: 100,000 * (80/100) = 80,000
- `fakeReach`: 100,000 - 80,000 = 20,000
- `budgetLoss`: 250,000 * (20,000 / 100,000) = $50,000 wasted
- `costPerGenuine`: 250,000 / 80,000 = $3.12 per user

**Step 3: Risk Classification (`riskService.ts`)**
- Score of 80 maps to `{ label: 'Shortlist', severity: 1 }`

**Step 4: Output Payload**
```json
{
  "genuineReach": 80000,
  "fakeReach": 20000,
  "budgetLoss": 50000,
  "costPerGenuineFollower": 3.125,
  "classification": {
    "label": "Shortlist",
    "severity": 1
  }
}
```

---

## Team Responsibilities

### Backend 2 (Team Member 3)
- **Responsibility:** Handle the financial logic, reach estimation, and influencer comparisons.
- **Input:** Influencer metrics + Authenticity Score (from Team Member 2) + Campaign Budget.
- **Output:** Financial loss metrics, genuine reach estimates, and comparative analysis objects.

---

## Input / Output Contracts

### Input Schema (`InfluencerInput`)
```typescript
export interface InfluencerInput {
  name: string;
  followers: number;
  engagementRate: number;
  authenticityScore: number; // 0-100 (Provided by Backend 1)
}
```

### Output Schema (`RiskMetrics`)
```typescript
export interface RiskMetrics {
  genuineReach: number;
  fakeReach: number;
  budgetLoss: number;
  costPerGenuineFollower: number;
  classification: {
    label: 'Shortlist' | 'Monitor' | 'Pause' | 'Reject';
    severity: number;
  };
}
```

---

## Integration & Setup

### How to Run
The system is built as a Node.js TypeScript module using CommonJS.

```bash
# 1. Install dependencies
npm install

# 2. Execute the engine
npx ts-node src/examples/usage.ts
```
