function [Sout,Pout] = primespiral(n,c)
% PRIMESPIRAL  Ulam's prime number spiral.
%   PRIMESPIRAL(n,c) plots the prime numbers in the n-by-n matrix
%   generated by storing c:c+n^2 in a spiral pattern starting in
%   the center.  The concentration of primes on some of the diagonals
%   is remarkable.  This phenomenon was discovered by Stanislaw Ulam
%   in 1963, and featured on the cover of Scientific American in
%   March, 1964.  For n <= 42, primespiral(n,c) shows the spiral 
%   numbering scheme.  The default value of c is 1.
%
%   With one or two output arguments,
%      S = primespiral(n,c), or
%      [S,P] = primespiral(n,c)
%   does no plotting, but returns S = prime spiral and P = isprime(S).
%
%   Examples:
%      primespiral(7)
%      primespiral(17,17)
%      primespiral(41,41)
%      primespiral(200)

%   Copyright 2014 Cleve Moler
%   Copyright 2014 The MathWorks, Inc.

if nargout > 0
   [Sout,Pout] = spiralprimes(n,c);
   return
end

if ~isequal(get(gcf,'name'),'Prime spiral')
   clf
   shg
   b(1) = uicontrol('sty','tog','uni','nor','pos',[.02 .02 .05 .05], ...
      'string','<','fontweight','bold','callback','primespiral(''<'')');
   b(2) = uicontrol('sty','tog','uni','nor','pos',[.08 .02 .05 .05], ...
      'string','-','fontweight','bold','callback','primespiral(''-'')');
   b(3) = uicontrol('sty','tog','uni','nor','pos',[.14 .02 .05 .05], ...
      'string','+','fontweight','bold','callback','primespiral(''+'')');
   b(4) = uicontrol('sty','tog','uni','nor','pos',[.20 .02 .05 .05], ...
      'string','>','fontweight','bold','callback','primespiral(''>'')');
   set(gcf,'name','Prime spiral','menu','none','numbertitle','off', ...
      'userdata',b);
   uicontrol('uni','nor','pos',[.90 .02 .08 .05], ...
      'string','close','callback','close(gcf)')
end
b = get(gcf,'userdata');

if nargin < 1, n = 200; end
if nargin < 2, c = 1; end
if isstr(n)
   if n ~= '<', set(b(1),'value',0), end
   if n ~= '>', set(b(4),'value',0), end
   c = get(b(1),'userdata');
   if n == '<' | n == '-', c = max(c-1,1); end
   if n == '>' | n == '+', c = c+1; end
   n = get(b(4),'userdata');
end
set(b(1),'userdata',c)
set(b(4),'userdata',n)

while c >= 1
   [S,P] = spiralprimes(n,c);
   spydetail(S,P)
   title(['c = ' int2str(c)])
   xlabel([int2str(nnz(P)) ' primes'])
   drawnow
   if get(b(1),'value'), c = max(c-1,1); end
   if get(b(4),'value'), c = c+1; end
   set(b(1),'userdata',c)
   if get(b(1),'value') == 0 & get(b(4),'value') == 0
      break
   end
end
if c == 1
   set(b(1:2),'enable','off')
else
   set(b(1:2),'enable','on')
end
set(b([1 4]),'value',0)


% ------------------------

function [S,P] = spiralprimes(n,c)
% SPIRALPRIMES
%   [S,P] = spiralprimes(n,c) returns two n-by-n matrices.
%   S is the spiral numbering of c:c+n^2-1.
%   P is true for the primes in S.

m = n^2-1+c;
P = zeros(m,1);
P(primes(m)) = 1;
S = spiral(n)+c-1;
P = reshape(P(S(:)),n,n);


% ------------------------

function S = spiral(n)
%SPIRAL SPIRAL(n) is an n-by-n matrix with elements
%   1:n^2 arranged in a rectangular spiral pattern.

S = [];
for m = 1:n
   S = rot90(S,2);
   S(m,m) = 0;
   p = m^2-m+1;
   v = (m-1:-1:0);
   S(:,m) = p-v';
   S(m,:) = p+v;
end
if mod(n,2)==1
   S = rot90(S,2);
end


% ------------------------

function spydetail(S,P)
% SPYDETAIL
%   SPYDETAIL(S,P) is like SPY(P) with the element values from S.

[n,n] = size(P);
if n <= 42
   delete(gca)
   axis([0 n+1 0 n+1])
   axis square
   axis ij
   for i = 1:n
      for j = 1:n
         if P(i,j)
            color = [0 0 1];
            fs = max(1,floor(16-2*log2(n)));
         else
            color = [1/3 1/3 1/3];
            fs = max(1,floor(16-3*log2(n)));
         end
         text(j,i,int2str(S(i,j)),'fontsize',fs,'color',color)
      end
   end
else
   if n <= 500, ms = 6; else, ms = 1; end
   [i,j] = find(P);
   plot(j,i,'.','markersize',ms)
   axis([0 n+1 0 n+1])
   axis square
   axis ij
end
