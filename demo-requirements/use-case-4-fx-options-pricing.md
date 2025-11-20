# Use Case 4: FX Options Pricing & Risk Management System

## The Requirement

### Overview
Build a real-time FX options pricing and risk management system for a trading desk that handles exotic options, calculates Greeks, manages portfolio risk, and provides mark-to-market valuations across multiple currency pairs.

### Functional Requirements

#### Core Features
1. **Options Pricing Engine**
   - Vanilla options (European, American)
   - Exotic options (Barriers, Digitals, Asian, Lookback)
   - Multiple pricing models (Black-Scholes, Garman-Kohlhagen, Local Vol, Stochastic Vol)
   - Smile interpolation and extrapolation
   - Vol surface construction

2. **Greeks Calculation**
   - First-order: Delta, Gamma, Vega, Theta, Rho
   - Second-order: Vanna, Volga, Charm, Veta
   - Bump-and-reprice and analytical methods
   - Greeks aggregation across portfolios

3. **Risk Management**
   - Real-time P&L calculation
   - VaR (Value at Risk) - Historical, Parametric, Monte Carlo
   - Stress testing and scenario analysis
   - Limit monitoring and breach alerts

4. **Market Data Integration**
   - Real-time spot rates from multiple providers
   - Volatility surfaces from broker feeds
   - Interest rate curves (OIS, LIBOR successors)
   - Dividend and forward points

5. **Position Management**
   - Trade capture and booking
   - Position aggregation by currency pair, desk, entity
   - Netting and exposure calculation
   - Settlement and exercise management

### Technical Requirements
- Sub-millisecond pricing for vanilla options
- 10,000 positions repriced per second
- 99.99% uptime during trading hours
- Audit trail for all calculations
- C++/Python hybrid (C++ for pricing, Python for orchestration)

---

## Why Vibe Coding Fails

### The Scenario
A quant developer asks: *"Build me an FX options pricer with Greeks calculation"*

### What Actually Happens

#### Session 1: The Simple Start
```
Developer: "Create a Black-Scholes pricer for FX options"
AI: Creates basic Black-Scholes implementation

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
```

**Problems the AI doesn't know about:**
- FX options use Garman-Kohlhagen (two interest rates)
- Premium can be in domestic OR foreign currency
- Delta conventions vary (spot delta vs forward delta)
- Vol quotes are in different conventions (ATM DNS, RR, BF)

#### Session 2: Adding Greeks
```
Developer: "Add delta and gamma calculation"
AI: Adds analytical Greeks

def delta(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1)
```

**Problems:**
- Uses wrong delta convention (should be premium-adjusted for FX)
- Doesn't handle the "sticky strike" vs "sticky delta" distinction
- Gamma is in wrong units (should be per 1% spot move)
- No concept of spot delta vs forward delta

#### Session 3: Exotic Options
```
Developer: "Add barrier option pricing"
AI: Implements basic barrier formula

# But misses:
# - Discrete vs continuous monitoring
# - Window barriers
# - Rebates
# - Double barriers
# - Quanto adjustments
```

#### Week 3: Production Disaster

**Trader**: "Why is my delta hedge wrong?"

**Investigation reveals:**
1. Delta convention mismatch with market standard
2. Vol surface interpolation is linear (should be cubic)
3. Forward points not included in pricing
4. Premium currency confusion losing $50K per trade
5. Theta calculated for calendar days, not business days

**Risk Manager**: "Your VaR numbers don't match our other systems"

**Because:**
- Historical VaR uses wrong return calculation
- Correlation matrix not positive semi-definite
- Vol scaling uses wrong day count
- No distinction between instantaneous and holding period risk

### The Cost of Getting It Wrong

```
Day 1: Trader executes $100M notional barrier option
Day 2: Delta hedge based on wrong Greeks
Day 3: Spot moves 1%, hedge P&L doesn't offset option P&L
Day 4: $500K unexplained P&L
Day 5: Risk flags portfolio for manual review
Day 6: Discovery - pricing model has fundamental errors

Result: $500K loss + trading desk shut down for 2 weeks
```

### Why Quant Finance is Different

1. **Conventions are everything**: Same formula, different conventions = different numbers
2. **Edge cases ARE the business**: Barriers, exercise, settlement
3. **Small errors compound**: 0.1% pricing error × $100M × 1000 trades = disaster
4. **No do-overs**: Once traded, you own the risk

---

## Why Spec Kit Wins

### Phase 1: Domain Analysis (Week 1)

```bash
npx spec-kit analyze --domain=fx-options
```

**Extracts critical domain knowledge:**

```markdown
## FX Options Domain Specification

### Pricing Conventions
1. **Garman-Kohlhagen Model**
   - Domestic rate (rd) and foreign rate (rf)
   - S = spot rate (domestic per foreign)
   - Premium in domestic currency (default) or foreign

2. **Delta Conventions**
   - Spot Delta: ∂V/∂S
   - Forward Delta: e^(-rf*T) * ∂V/∂S
   - Premium-Adjusted Delta: Delta - V/S
   - Market quotes use premium-adjusted forward delta

3. **Volatility Surface**
   - ATM: Delta-neutral straddle (DNS)
   - Risk Reversal: 25Δ call vol - 25Δ put vol
   - Butterfly: (25Δ call + 25Δ put)/2 - ATM
   - Interpolation: SABR or SVI parameterization

### Business Day Conventions
- Spot date: T+2 (except USD/CAD = T+1)
- Option expiry: 10am NY cut (default)
- Delivery: Spot date from expiry
- Theta: Per business day, not calendar day

### Greeks Standards
- Delta: Percentage of foreign notional
- Gamma: Per 1% spot move
- Vega: Per 1 vol point (absolute)
- Theta: Per business day
```

### Phase 2: Corporate Guidelines (Week 1)

```bash
npx spec-kit guidelines
```

**Output: QUANT-GUIDELINES.md**

```markdown
## Quantitative Development Standards

### Numerical Precision
- ALL pricing in Decimal (not float) for currencies
- Greeks calculated to 8 significant figures
- Vol surface interpolation: Cubic spline minimum

### Testing Requirements
- Every pricer: test against Bloomberg OVML
- Greeks: bump test vs analytical (tolerance 1e-6)
- Edge cases: deep ITM, deep OTM, near expiry

### Convention Handling
- ALWAYS specify delta convention in function signature
- ALWAYS specify premium currency
- NEVER hardcode day counts (ACT/365, ACT/360, 30/360)

### Validation
- Vol surface: Check for arbitrage (butterfly spread > 0)
- Correlation matrix: Positive semi-definite check
- Forward points: Consistency with interest rates

### Audit Trail
- Log all pricing inputs and outputs
- Version all model parameters
- Record market data timestamps
```

### Phase 3: Specification with Financial Precision (Week 1-2)

```bash
npx spec-kit specify
```

**Output: Complete Quant Specification**

```markdown
## Options Pricing Engine Specification

### Vanilla Pricer Interface
```python
def price_vanilla_fx_option(
    option_type: Literal['call', 'put'],
    spot: Decimal,
    strike: Decimal,
    expiry: BusinessDate,
    domestic_rate: Curve,
    foreign_rate: Curve,
    vol_surface: VolSurface,
    notional: Decimal,
    notional_currency: Literal['DOM', 'FOR'],
    premium_currency: Literal['DOM', 'FOR'],
    delivery_date: Optional[BusinessDate] = None,
    cut_time: TimeZone = 'NY_10AM'
) -> PricingResult:
    """
    Returns:
        PricingResult with:
        - premium (in premium_currency)
        - spot_delta (premium-adjusted if premium_currency=FOR)
        - forward_delta
        - gamma (per 1% spot move)
        - vega (per 1 vol point)
        - theta (per business day)
        - rho_domestic, rho_foreign
    """
```

### Vol Surface Specification
```python
class VolSurface:
    """
    Construction from market quotes:
    - ATM DNS (delta-neutral straddle)
    - 25D RR, 10D RR (risk reversals)
    - 25D BF, 10D BF (butterflies)

    Interpolation:
    - Strike: SABR with beta=1
    - Time: Flat forward variance

    Validation:
    - Butterfly spreads > 0 (no arbitrage)
    - No negative forward variance
    """
```

### Barrier Option Specification
```python
def price_barrier_option(
    barrier_type: Literal['KI', 'KO'],  # Knock-in, Knock-out
    barrier_direction: Literal['up', 'down'],
    barrier_level: Decimal,
    monitoring: Literal['continuous', 'discrete'],
    monitoring_times: Optional[List[BusinessDate]],  # For discrete
    rebate: Decimal = 0,
    rebate_timing: Literal['hit', 'expiry'] = 'expiry',
    ...
) -> PricingResult:
    """
    Pricing model selection:
    - Continuous: Analytical (Rubinstein-Reiner)
    - Discrete: Monte Carlo with Brownian bridge

    Greeks:
    - Barrier delta includes probability of knock
    - Discontinuous gamma near barrier
    """
```
```

### Phase 4: Orchestrated Development (Weeks 2-6)

**Session 1: Core Pricing Framework**
- Implements Garman-Kohlhagen with all conventions
- Sets up vol surface construction
- **Context**: All FX conventions documented

**Session 2: Greeks Engine**
- Implements all Greeks with correct conventions
- Premium-adjusted delta for FX
- **Context**: Knows delta conventions from spec

**Session 3: Exotic Options**
- Barrier options with all monitoring types
- Digital options with spread approximation
- **Context**: Full specification of edge cases

**Session 4: Risk Aggregation**
- Portfolio-level Greeks
- VaR with proper correlation handling
- **Context**: All numerical standards applied

**Session 5: Market Data Integration**
- Vol surface building from broker quotes
- Curve construction with proper day counts
- **Context**: Convention specifications

### Validation Against Bloomberg

```python
# Automated validation against OVML
test_cases = [
    ("EUR/USD 1M ATM Call", bloomberg_price=0.0234, tolerance=0.0001),
    ("USD/JPY 3M 25D Put", bloomberg_price=0.0156, tolerance=0.0001),
    ("GBP/USD 6M KO Barrier", bloomberg_price=0.0089, tolerance=0.0002),
]

for test in test_cases:
    our_price = pricer.price(test.params)
    assert abs(our_price - test.bloomberg_price) < test.tolerance
```

**Result: All prices match Bloomberg within tolerance**

---

## Measurable Outcomes

| Metric | Vibe Coding | Spec Kit | Improvement |
|--------|-------------|----------|-------------|
| Development Time | 12 weeks | 6 weeks | **50% faster** |
| Pricing Errors Found | 15 (in prod) | 0 | **100% accuracy** |
| Trading Desk Downtime | 2 weeks | 0 | **No disruption** |
| P&L Breaks | $500K+ | $0 | **Zero losses** |
| Bloomberg Reconciliation | 73% pass | 100% pass | **Full accuracy** |
| Greeks Convention Errors | 8 issues | 0 | **Correct conventions** |
| Audit Findings | 12 | 0 | **Compliant** |

---

## Key Differentiator

### The Domain Expertise Problem
Quant finance has **decades of accumulated conventions**:
- Delta conventions that vary by market
- Day count conventions that affect calculations
- Premium currency that changes the Greeks
- Exercise styles with different pricing models
- Market quoting conventions vs calculation conventions

**Vibe coding**: AI uses textbook formulas that miss market conventions
**Result**: Prices that are mathematically correct but market-wrong

### The Spec Kit Solution

**Domain specification captures all conventions:**

```
FX Options Domain Knowledge
         ↓
    spec-kit analyze
         ↓
Convention Specification
    - Delta: premium-adjusted forward
    - Vol: SABR interpolation
    - Day count: ACT/365 for theta
         ↓
Development with Correct Conventions
         ↓
Prices Match Bloomberg ✓
```

**Every line of code follows market conventions because
they're specified before development begins.**

---

## Demo Script

### Setup (2 min)
"FX options pricing seems simple - it's just Black-Scholes, right? Let's see what happens when vibe coding builds a pricer..."

### Problem Demo (3 min)
Show vibe coding creating a pricer:
1. Basic Black-Scholes (not Garman-Kohlhagen)
2. Delta without premium adjustment
3. "This would be $500K wrong on a $100M trade"

### Solution Demo (5 min)
1. Show domain analysis extracting conventions
2. Show specification with delta convention handling
3. Show generated code with premium-adjusted delta
4. Show Bloomberg reconciliation: 100% pass

### Close (2 min)
"In quant finance, conventions are everything. A textbook formula with wrong conventions is worse than no formula. Spec Kit ensures every calculation follows market standards. That's the difference between a working trading desk and a $500K loss."
