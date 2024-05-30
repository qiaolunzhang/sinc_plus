
param n;
#physical nodes and links
set N ordered:=1..n;
set E within {i in N, j in N: i<j};

#number of virtual networks
param num_top;
#set of virtual networks
set V:=1..num_top;

#logical nodes and links
set Nl{v in V} within N ordered;
set El{v in V} within Nl[v] cross Nl[v];

#set with virtual links of all virtual networks
set Eltot:=setof{v in V, (s,t) in El[v]} (v,s,t);

# set containing bidirectional physical links
set A within {N,N} := E union setof{(i,j) in E} (j,i);


# set containing bidirectional logical links of VNs
set B{v in V} within {Nl[v],Nl[v]} := El[v] union setof{(s,t) in El[v]} (t,s);


# set containing bidirectional logical links divided for each VN
set Btot:= setof{v in V, (s,t) in B[v]} (v,s,t);

#Arc capacity
param cap{A};

#parameter and sets useful to find the cut-sets of the logical topologies
param m{v in V}:= card(Nl[v]);
set S{v in V} := 0 .. (2**m[v] -1);
set S2{v in V,k in S[v]} := {i in Nl[v] : (k div 2**(ord(i)-1)) mod 2 = 1};


#CUTSET of the logical topologies
set SUBE{v in V, k in S[v]} := {s in S2[v,k], t in Nl[v] diff S2[v,k]: (s,t) in El[v] or (t,s) in El[v]};
set SUBE2tot{v in V, k in S[v]} := {(s,t) in El[v]: (s,t) in SUBE[v,k] or (t,s) in SUBE[v,k]};

#Number of double link failures combinations
param comb default 0;
set F := 0..comb;
#Combinations of double link failures of physical network
set DF{k in F} within N cross N default {};

#directed flow variable, used for mapping virtual links in the physical network
var q{A,Btot} binary;
#undirected flow variable
var qa{E,Eltot} binary;

#virtual link affected by a failure as a conseguence of a physical link down
var g{Eltot,F} binary;

#cut-set of a virtual network down
var r{v in V,S[v] diff{0,2**m[v]-1},F} binary;
#virtual network down
var av{V,F} binary;


	
	# TOTAL WAVELENGTH CONSUMPTION
#minimize TWC: sum{(i,j) in A, (v,s,t) in Btot} q[i,j,v,s,t];
minimize TWC: 100*(sum{(i,j) in A, (v,s,t) in Btot} q[i,j,v,s,t]) - 0.1*( (num_top*(comb+1)) - (sum{k in F, v in V} av[v,k]) );


# flow balancing constraint for mapping
s.t. flow {(v,s,t) in Btot, i in N: i=s}:
	sum{(i,j) in A} q[i,j,v,s,t] - sum{(j,i) in A} q[j,i,v,s,t] = 1;
	
s.t. flow1 {(v,s,t) in Btot, i in N: i=t}:
	sum{(i,j) in A} q[i,j,v,s,t] - sum{(j,i) in A} q[j,i,v,s,t] = -1;
	
s.t. flow2 {(v,s,t) in Btot, i in N: i<>s and i<>t}:
	sum{(i,j) in A} q[i,j,v,s,t] - sum{(j,i) in A} q[j,i,v,s,t] = 0;
	
	

# biderectional wavelength assignment
s.t. bidirectionality {(v,s,t) in Btot, (i,j) in A}:
	q[i,j,v,s,t]-q[j,i,v,t,s]=0;

s.t. bidirectionality2 {(v,s,t) in Btot, (i,j) in A}:
	q[i,j,v,s,t]+q[j,i,v,s,t]<=1;
	


# xor needed for improving computational time of survivability
s.t. flow3 {(i,j) in E, (v,s,t) in Eltot}:
	qa[i,j,v,s,t] >= q[i,j,v,s,t]-q[j,i,v,s,t];
	
s.t. flow4 {(i,j) in E, (v,s,t) in Eltot}:
	qa[i,j,v,s,t] >= q[j,i,v,s,t]-q[i,j,v,s,t];
	
s.t. flow5 {(i,j) in E, (v,s,t) in Eltot}:
	qa[i,j,v,s,t] <= q[i,j,v,s,t]+q[j,i,v,s,t];

s.t. flow6 {(i,j) in E, (v,s,t) in Eltot}:
	qa[i,j,v,s,t] <= 2 - q[i,j,v,s,t]-q[j,i,v,s,t];
	
	

# SURVIVABILITY constraint
s.t. survivability {(i,j) in E, v in V, k in S[v] diff {0,2**m[v]-1}}:
	sum{(s,t) in SUBE2tot[v,k]} qa[i,j,v,s,t] <= card(SUBE2tot[v,k])-1;

	
#s.t. capacity{(i,j) in A}:
#	sum{(v,s,t) in Btot} q[i,j,v,s,t]<= cap[i,j];	


#Virtual links down due to a double physical link failure
s.t. downVirLinks{(v,s,t) in Eltot, k in F, (i,j) in DF[k]}:
	g[v,s,t,k] >= qa[i,j,v,s,t];	

s.t. downVirLinks2{(v,s,t) in Eltot, k in F}:
	g[v,s,t,k] <= sum{(i,j) in DF[k]} qa[i,j,v,s,t];	


# AVAILABILITY constraints

# Constraints that set the cut-sets down for each failing set
s.t. cutsetsDown{v in V, h in S[v] diff {0,2**m[v]-1}, k in F, (s,t) in SUBE2tot[v,h]}:
	r[v,h,k] <= g[v,s,t,k];
		
s.t. cutsetsDown2{v in V, h in S[v] diff {0,2**m[v]-1}, k in F}:
	r[v,h,k] >= (sum{(s,t) in SUBE2tot[v,h]} g[v,s,t,k]) - (card(SUBE2tot[v,h]) -1);

#A virtual network is considered disconnected if at least a cut-set of that 
#VN is down (VN separated at least in two different parts)
s.t. virtNetDown{v in V, h in S[v] diff {0,2**m[v]-1}, k in F}:
	av[v,k] >= r[v,h,k];

s.t. virtNetDown2{v in V, k in F}:
	av[v,k] <= sum{h in S[v] diff {0,2**m[v]-1}} r[v,h,k];