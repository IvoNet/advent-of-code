# Visualisation

# Explode action

- has precedence over split action

```text
[7, [6, [5, [4, [3, 2]]]]]

        p0
     /     \
   l=7      p1
          /    \
         6      p2
              /    \
             5      p3
                  /   \
                 4     p4
                      / \
                     3   2   < reduce (explode)
- 2 no right => 0

        p0
     /     \
   l=7      p1
          /    \
         6      p2
              /    \
             5      p3
                  /   \
                 4     p4
                      / \
                     3   0

- p4 left (3) add with first value left
  if p3.left has value then add => p3.left := 4 + 3 = 7
  - p4 has been resolved so its value need to be moved up
  - p3.right := p4.right and p4.right_pair := None

        p0
     /     \
   l=7      p1
          /    \
         6      p2
              /    \
             5      p3
                  /   \
                 7     0
                 
[7,[6,[5,[7,0]]]]
```

```text


[[6,[5,[4,[3,2]]]],1]

               p0
             /   \
            p1     1
         /    \
        6      p2
             /   \
            5     p3
                /  \
               4    p4 
                   / \
                  3   2  <- reduce

left (3)
   if parent.left != None
      p3.left := 3 + 4 = 7
      p4.left := None


               p0
             /   \
            p1     1
         /    \
        6      p2
             /   \
            5     p3
                /  \
               7    p4 
                   / \
                  -   2  <- reduce


right (2)
   p3.right_parent != None so ask its parent (recursively) until no right 
   parent and see if that parent has right value 
        - p0.right := 2 + 1
     
               p0
             /   \
            p1     3
         /    \
        6      p2
             /   \
            5     p3
                /  \
               7    p4 
                   / \
                  -   -  <- reduce
        - P4 collapses and has no values so P3.right := 0
               p0
             /   \
            p1     3
         /    \
        6      p2
             /   \
            5     p3
                /  \
               7    0
 - explode done = True                   
[[6,[5,[7,0]]],3]
```

## Split action

- left down rounded // 2
- right = orig - left (up rounded)

```text

```

# Sum example

```text
[[[[4,3],4],4],[7,[[8,4],9]]] + [1,1]

0            p (orig)           p (new)
           /   \               / \
1         p     p             1   1
        /  \   / \      +
2      p    4 7   p
      / \        / \
3    p   4      p   9
    / \        / \
   4   3      8   4     


first action: addition

- new Pair (depth 0) 
    - with left_pair the original pair 
    - with right the new pair 

0                  p (top)
              /        \
1            p (orig)   p (new)
           /   \       / \
2         p     p     1   1
        /  \   / \   
3      p    4 7   p
      / \        / \
4    p   4      p   9
    / \        / \
   4   3      8   4     

- all original pairs (left_pair) have a new depth +1     
- the orig needs to have its parent assigned to the new top pair
    - top.left_pair.parent := top
    - top.right_pair.parent := top  

Noe that the addition is done and all settings corrected we can reduce it
- we have a depth >= 4 (two actually but one action at the time)

second action: explode

0                  p (top) 
              /        \
1            p          p  
           /   \       / \
2         p     p     1   1
        /  \   / \   
3      p    4 7   p
      / \        / \
4    p   4      p   9
    / \        / \
   4   3 <-R! 8   4 <-R!    

- actual explosion happens when:
    - a depth >= 4
    - our left and right values not empty
  - so we call explode(top) but the top has no depth of >= 4
    - first walk left!
        - if top.left_pair:
            - explode(that one) etc (recursive)
            return its boolean value if changed
    - then walk right
        - if top.right_pair:
            - explode(that one) etc (recursive)
            return its boolean value if changed
    if none apply then return False as no explode action was performed

  - explosion: 
     - after walking left for a while (see above)
       - we find an explodeable pair:
         explode it
         
0                  p (top) 
              /        \
1            p          p  
           /   \       / \
2         p     p     1   1
        /  \   / \   
3      p    4 7   p
      / \        / \
4   *0  *7      p   9
               / \
              8   4  <-R!   
       - return True as we have an explosion
     - new action round: explode     
       - 
0                  p (top) 
              /        \
1            p          p  
           /   \       / \
2         p     p     1   1
        /  \   / \   
3      p    4 15  p
      / \        / \
4    0   7      p   13
               / \
              -   -     
when done
0                  p (top) 
              /        \
1            p          p  
           /   \       / \
2         p     p     1   1
        /  \   / \   
3      p    4 15* p
      / \        / \
     0   7      0   13*
    - return True
    - try exploding again results in False
    - try splitting it
      - after walking left then right a couple of time we find the 15 value left
        split it
                  
0                    p (top) 
                /            \
1              p              p  
           /       \         / \
2         p         p       1   1
        /  \       /   \   
3      p    4     p     p
      / \        / \   / \
     0   7      7   8 0   13*
     - return True on splittit
     - try exploding again: False
     - try splittit again
     
0                    p (top) 
                /            \
1              p              p  
           /       \         / \
2         p         p       1   1
        /  \       /   \   
3      p    4     p     p
      / \        / \   / \
4    0   7      7   8 0   p <-Explode
                         / \                                              
                        6   7
     - return True on split
     - Try expoding again

intermediary state     
0                    p (top) 
                /            \
1              p              p  
           /       \         / \
2         p         p      *8   1
        /  \       /    \   
3      p    4     p      p
      / \        / \    / \
4    0   7      7   8 *6   p <-Explode
                          / \                                              
                         -   -
final state                        
0                    p (top) 
                /            \
1              p              p  
           /       \         / \
2         p           p    *8   1
        /  \       /    \   
3      p    4     p      p
      / \        / \    / \
4    0   7      7   8 *6   0
                        
     - Return True on Explode
     - Try exploading again: False
     - Try splitting again: False
     Done!

[[[[0,7],4][[7,8][6,0]],[8,1]]]
                        
```

```python
    def test_explode_1(self):
    pair = parse([[[[[9, 8], 1], 2], 3], 4])
    self.assertEqual(True, explode(pair))


def test_explode_2(self):
    self.assertEqual([7, [6, [5, [7, 0]]]], explode([7, [6, [5, [4, [3, 2]]]]]))


def test_explode_3(self):
    self.assertEqual([[6, [5, [7, 0]]], 3], explode([[6, [5, [4, [3, 2]]]], 1]))


def test_explode_4(self):
    self.assertEqual([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
                     explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]))


def test_explode_5(self):
    self.assertEqual([[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
                     explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]))


def test_split_1(self):
    self.assertEqual([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]],
                     splitit([[[[0, 7], 4], [15, [0, 13]]], [1, 1]]))

```
