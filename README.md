# HoshinoAI-EarthHack
-> You take a list of business pitches
-> We evaluate them in terms of resources used in trinary terms {-1, 0 ,1} for resource impact
    -> Do this by shoving ideas into LLMs and getting them to spit out some output text that summarizes resource impact.
    -> Then convert the output text into a numerical value for each resource involved and cache away the initial output text somewhere.
    -> Do this for all pitches, see how many distinct resources you have, and shove all of the data into a vector. {idea, r1, r2, ..., rn} (ri \in {-1, 0 ,1})
-> Now we do actual math. 

Suppose we have a set of vectors {v_1, ..., v_n} with each vector representing a pitch idea. 
We can do one of two things:
- Utilitarian evaluation
    - Select the greatest set of vectors where a = v_i + ... + v_j and the norm of a is minimized when ignoring the first element of all v_i. 
    - Perhaps provide a list of different sets if possible.
- Recycling 
    - Treat each vector like a vertex in a graph and ideally attempt to find Hamiltonian cycles.
    - Find subgraphs where instances of r_ij + r_jk = 0 is maximized. Surely this is horrendous.

 