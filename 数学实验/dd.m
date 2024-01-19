function y=dd(f2,x,n)
p=[x];
for i=2:n
    p(i)=f2(p(i-1));
end
end

