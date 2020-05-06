### 考察

結局はどういう時は変更できるかを考えると

まず $k \le n/2$以下では必ず変更できる.

なぜなら

$x_i \neq x_{i+1}$の時,
$x_{i-n/2}$か$x_{i+1+n/2}$のどちからが存在し,
$n/2$個変更し,$x_i$と$x_{i+1}$を同じ数値にできる,
これを左から行うと$i \le n - k/2$の時は$x_1, \ldots, x_i$の値が一致するように取れる.
さらに$i > n - k/2$の場合は$x_{i-k}, \ldtos, x_{i-1}$を含んで変更するため,$x_{i-k}$と$x_{i-k-1}$の値が異なるが,この場合は$x_{i-k-1}, \ldtos, x_{i+1}$までを値を変更することにより.$x_{i+1}$まで同じ値にできる.

では$k \ge 2/n + 1$の時はそうできるとは限らない.
$1$から数値を変更しようとも$n$から数値を変更しようとも必ず含まれる$x_{n-k}, x_{n-k+1}, \ldots, x_{k+1}$が同じ値である必要がある.
それ以外の値が異なっていても,
上と同様に$k$個と$k+1$個の値を入れ替えることにより数値を一致させられる.
よってこれが一致する最大の$k$が求めるものである.
これは例えば真ん中の値,(これは偶・奇で異なる)に対して,一つずつ値をずらし,値が一致するかで計算することができる.


```python
S = input()
l = len(S)
if l % 2 == 0:
    ans = l // 2
    after_half = l//2
    before_half = after_half - 1
    s = S[l//2]
    for i in range(l//2):
        if S[before_half] == S[after_half] and S[before_half] == s:
            ans += 1
            before_half -= 1
            after_half += 1
        else:
            break
if l % 2 == 1:
    ans = l // 2 
    after_half = l//2
    before_half = after_half
    s = S[l//2]
    for i in range(l//2 + 1):
        if S[before_half] == S[after_half] and S[before_half] == s:
            ans += 1
            before_half -= 1
            after_half += 1
        else:
            break

print(ans)
```