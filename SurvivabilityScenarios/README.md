## Errors in the previous code

- Error in calculating the availability: we need to ensure that
  the cutsets and the mapping should be from the same VN.
```python
def get_availability_cutsets_total(totCut, totMaps):
    pass
```

- Error in constructing new nodes: in the code, it directly check
  the number of characters in the node name. However, it only works
  when the node name is a single character.
```python
for i, j, k in nestedList:
    if i in cnodes and j in cnodes:
        C.remove_edge(i, j)  # k)
        C.add_edge(newNode, newNode, key=k)

    elif i in cnodes and j not in cnodes:

        if nodeTotal == len(str(abs(newNode))):
            C.add_edge(newNode, newNode, key=k)

            C.remove_edge(i, j)
        else:
            C.add_edge(newNode, j, key=k)

            C.remove_edge(i, j)
```

- Logic error in calculating the availability with spare slice: 
  there should be multiple links between the same node pair to 
  takes into account of different mapping of the virtual link

- Error in constructing the cycles: the code should consider that
  which edge to select among the multiple edges between the same
  node pair. This is captured in contractedLink3