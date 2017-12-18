# a\
# | c -- d
# b/
#

color(a;1) :- vertex(a), not color(a;2), not color(a;3).
color(a;2) :- vertex(a), not color(a;1), not color(a;3).
color(a;3) :- vertex(a), not color(a;1), not color(a;2).

color(b;1) :- vertex(b), not color(b;2), not color(b;3).
color(b;2) :- vertex(b), not color(b;1), not color(b;3).
color(b;3) :- vertex(b), not color(b;1), not color(b;2).

color(c;1) :- vertex(c), not color(c;2), not color(c;3).
color(c;2) :- vertex(c), not color(c;1), not color(c;3).
color(c;3) :- vertex(c), not color(c;1), not color(c;2).

color(d;1) :- vertex(d), not color(d;2), not color(d;3).
color(d;2) :- vertex(d), not color(d;1), not color(d;3).
color(d;3) :- vertex(d), not color(d;1), not color(d;2).

:- edge(a;b), color(a;1), color(b;1).
:- edge(a;b), color(a;2), color(b;2).
:- edge(a;b), color(a;3), color(b;3).

:- edge(a;c), color(a;1), color(c;1).
:- edge(a;c), color(a;2), color(c;2).
:- edge(a;c), color(a;3), color(c;3).

:- edge(b;c), color(b;1), color(c;1).
:- edge(b;c), color(b;2), color(c;2).
:- edge(b;c), color(b;3), color(c;3).

:- edge(c;d), color(c;1), color(d;1).
:- edge(c;d), color(c;2), color(d;2).
:- edge(c;d), color(c;3), color(d;3).

vertex(a).
vertex(b).
vertex(c).
vertex(d).

edge(a;b).
edge(a;c).
edge(b;c).
edge(c;d).

# expected solutions used for checking correctness
S = {color(a;3), color(b;2), color(c;1), color(d;3), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;3), color(b;2), color(c;1), color(d;2), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;3), color(b;1), color(c;2), color(d;3), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;3), color(b;1), color(c;2), color(d;1), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;2), color(b;3), color(c;1), color(d;3), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;2), color(b;3), color(c;1), color(d;2), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;2), color(b;1), color(c;3), color(d;2), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;2), color(b;1), color(c;3), color(d;1), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;1), color(b;3), color(c;2), color(d;3), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;1), color(b;3), color(c;2), color(d;1), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;1), color(b;2), color(c;3), color(d;2), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
S = {color(a;1), color(b;2), color(c;3), color(d;1), edge(a;b), edge(a;c), edge(b;c), edge(c;d), vertex(a), vertex(b), vertex(c), vertex(d)}
