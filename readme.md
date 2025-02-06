# Cointegration Pair Trading
### Premise
The basic premise of this approach is too find pairs of assets that pass the Engle-Grainger cointegration test with sufficient confidence interval such that the spread between the two assets can be considered statistically stationary or 'mean-reverting'. 

$s_t = y_t - \beta x_t$ 

Cointegration implies co-movement between two assets that behaves liek a kind of equilibrium over time. With a constant mean, a trading opportunity can arise if the spread as defined below, deviates from the mean at extreme levels i.e.  ± $\sigma$ or ± $2\sigma$. 

If the spread is currently trading at + $\sigma$, then sell the spread hoping to profit from the spread reverting to the mean. If the spread is currently $-2\sigma$ away from the mean, then buy the spread hoping to profit from a rising spread till the mean. 

Many variations exist around this general idea in terms of entries and exits once a cointegrated pair has been established. 

Finally, $\beta$ or the hedge ratio can be found by regressing the price data $y_t$ vs $x_t$. 

### Implementation
- I pulled daily close data using the `yfinance` and `polygon.api` interfaces
- `statsmodels.tsa.stattools` has a function `coint` that takes two price timeseries and return the p-value (probability of null hypothesis being true). The lower the p-value the higher the probability the 2 timeseries are cointegrated.
- I used a simple OLS scheme to determine $\beta$ but more sophisticated implementations exist i.e. TLS, RANSAC
- Every possible combination is checked, code can run slow as runtime scales with number of combinations. For 100 stocks there are 100C2 = 4950 pairs. I've taken a view to focus the input list to stocks that are from the same geography and or industry. 

### Pairs Found

- 04-Feb-2025
    * BARC.L - (0.88) $\cdot$ BREE.L; [Short] Current Level: -88, Target Level: -140, Exit Level: OPEN_TRADE
    * DGN.L  - (0.84) $\cdot$ KGF.L; [Short] Current Level: 221, Target Level: 170, Exit Level: OPEN_TRADE
    * FGP.L - (2.7) $\cdot$ ESP.L; [Short] Current Level: -61, Target Level: -85, Exit Level: OPEN_TRADE


### To Do
- Implement TLS for determining the hedge ratio
- try other geographies i.e. France, Germany, Netherlands, Spain, Selected US industries

