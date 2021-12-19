# 2d draw

--- scanner 0 --- 0,2 ...B. s0 = 0,0 4,1 B.... s1 = ?,? 3,3 ....B S.... ---
scanner 1 --- -1,-1 ...B.. -5,0 B....S -2,1 ....B.

3 matches ...B.. diff = abs 0 + abs 1 0,2 -> -5,0 B....S1 abs(x0)+abs(x1), abs(
y0)+abs(y1)
4,1 -> -1,-1 ....B.        (0+5,2+1) -> 5,2 3,3 -> -2,1 S..... 0

ordering not the same though
