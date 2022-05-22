expense_stream_data
cvx_begin % no investments
variables x(m) b(n) w(n)
minimize(b(1) + sum(x))
w + P*x == e
x == 0
b >= 0
for t = 1:n-1
b(t+1) == (1+rho)*b(t) - w(t)
end
cvx_end
total_cost_no_investments = cvx_optval