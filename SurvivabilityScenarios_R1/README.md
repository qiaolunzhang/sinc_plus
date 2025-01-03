## Generate data files

- **7-node german topology**: 
  - generate_ampl_data_file_survivability_german.py

- **tokyo topology**:
  - generate_ampl_data_file_survivability_tokyo.py

## Obtain the results

- **7-node german topology**:
  - sinc_loop_german_paper_per_instance_5nodesVN_Paper.sh
  - sinc_loop_german_paper_per_instance_5nodesVN_SP.sh

- **tokyo topology**:
  - sinc_loop_tokyo_paper_per_instance_5nodesVN_Paper.sh

## Note about different cases

1 - SVNM (min. TWC) 
2 - SVNM (max AV) 
3 - Two-step SINC (min TWC) 
4 - Two-step SINC (max AV) 
5 - One-step SINC (min TWC) 
6 - One-step SINC (max AV) 


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

- Error in updating the new mapping in local search algorithm: 
  we can update when AV_new > AV_old and TWC_new <= TWC_old
  rather than only TWC_new = TWC_old

- Error in deciding the failed links when checking the resiliency
  under double-link failures: we need to check both directions of
  the link

- Error for settings of bounds of the ILP: the bound should be as 
  as possible, since the TWC and AV has a very different weight