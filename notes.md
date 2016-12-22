Beta: Slope of linear fit between stock and the market i.e. how reactive it is to the market

Alpha: y-intercept of linear fit between stock and market

Equation:

Stock price = Beta * Market price + Alpha
Slope != Correlation
Correlation = How tightly the scatterplot fits the linear fit

Daily Portfolio Value
1. Normalize the prices
2. Multiply by allocations
3. Multiply by start value

normed = prices / prices[0]
alloced = normed * allocations
pos_vals = alloced * start_val (1million)
port_val = pos_vals.sum(axis=1)

Statistics

Ignore first 0 daily return with: daily_rets = daily_rets[1:]

Cumulative return = (port_val[-1] / port_val[0] - 1)
Average daily return = daily_rets.mean()
Standard deviation = daily_rets.std()

Sharpe Ratio = risk adjusted return
also considers risk free rate of return

S = mean(daily_rets - daily risk free) / std(daily_rets - daily risk free)
3 mo Treasury bill?

daily risk free rate = 252 root of (1.0 +.1) - 1
--for all intents and purposes

Sharpe Ratio can change depending on frequency of sample
SR is annual measure
SR annualized = k * SR
k = sqrt(# of samples / yr)
daily k = sqrt(252)
weekly k = sqrt(52)
monthly k = sqrt(12)



