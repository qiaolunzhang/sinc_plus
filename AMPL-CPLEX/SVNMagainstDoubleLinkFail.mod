
param n;
#physical nodes and links
set N ordered:=1..n;
set E within {i in N, j in N: i<j};

#number of virtual networks
param num_top;
#set of virtual networks
set TOP:=1..num_top;

#logical nodes and links
set Nl{top in TOP} within N ordered;
set El{top in TOP} within Nl[top] cross Nl[top];

#set with virtual links of all virtual networks
set Eltot:=setof{top in TOP, (s,t) in El[top]} (top,s,t);

# set containing bidirectional physical links
set A within {N,N} := E union setof{(i,j) in E} (j,i);

# set containing bidirectional logical links of VNs
set B{top in TOP} within {Nl[top],Nl[top]} := El[top] union setof{(s,t) in El[top]} (t,s);

# set containing bidirectional logical links divided for each VN
set Btot:= setof{top in TOP, (s,t) in B[top]} (top,s,t);


#Arc capacity
param cap{A};

#parameter and sets useful to find the cut-sets of the logical topologies
param m{top in TOP}:= card(Nl[top]);
set POWERSET2{top in TOP} := 0 .. (2**m[top] -1);
set S2{top in TOP,k in POWERSET2[top]} := {i in Nl[top] : (k div 2**(ord(i)-1)) mod 2 = 1};


#CUTSET of the logical topology
set SUBE{top in TOP, k in POWERSET2[top]} := {s in S2[top,k], t in Nl[top] diff S2[top,k]: (s,t) in El[top] or (t,s) in El[top]};
set SUBE2tot{top in TOP, k in POWERSET2[top]} := {(s,t) in El[top]: (s,t) in SUBE[top,k] or (t,s) in SUBE[top,k]};

#Number of double link failures combinations
param comb default 0;
set COMB := 0..comb;
#Combinations of double link failures of physical network
set DF{k in COMB} within N cross N default {};

#directed flow variable, used for mapping virtual links in the physical network
var q{A,Btot} binary;
#undirected flow variable
var qa{E,Eltot} binary;

#virtual link affected by a failure as a conseguence of a physical link down
var vld{Eltot,COMB} binary;

#cut-set of a virtual network down
var avc{top in TOP,POWERSET2[top] diff{0,2**m[top]-1},COMB} binary;
#virtual network down
var av{TOP,COMB} binary;

#flow variable equal to 1 if virtual link (s,t) is mapped on physical link (i,j)
#or on physical link (a,d)
var l{A,A,Btot} binary;

	
	# TOTAL WAVELENGTHS CONSUMPTION
minimize TWC: sum{(i,j) in A, (top,s,t) in Btot} q[i,j,top,s,t];


# flow constraint for mapping
s.t. flow {(top,s,t) in Btot, i in N: i=s}:
	sum{(i,j) in A} q[i,j,top,s,t] - sum{(j,i) in A} q[j,i,top,s,t] = 1;
	
s.t. flow1 {(top,s,t) in Btot, i in N: i=t}:
	sum{(i,j) in A} q[i,j,top,s,t] - sum{(j,i) in A} q[j,i,top,s,t] = -1;
	
s.t. flow2 {(top,s,t) in Btot, i in N: i<>s and i<>t}:
	sum{(i,j) in A} q[i,j,top,s,t] - sum{(j,i) in A} q[j,i,top,s,t] = 0;
	
	

# biderectional wavelength assignment
s.t. bidirectionality {(top,s,t) in Btot, (i,j) in A}:
	q[i,j,top,s,t]-q[j,i,top,t,s]=0;

s.t. bidirectionality2 {(top,s,t) in Btot, (i,j) in A}:
	q[i,j,top,s,t]+q[j,i,top,s,t]<=1;
	


# xor needed for improving computational time of survivability
s.t. flow3 {(i,j) in E, (top,s,t) in Eltot}:
	qa[i,j,top,s,t] >= q[i,j,top,s,t]-q[j,i,top,s,t];
	
s.t. flow4 {(i,j) in E, (top,s,t) in Eltot}:
	qa[i,j,top,s,t] >= q[j,i,top,s,t]-q[i,j,top,s,t];
	
s.t. flow5 {(i,j) in E, (top,s,t) in Eltot}:
	qa[i,j,top,s,t] <= q[i,j,top,s,t]+q[j,i,top,s,t];

s.t. flow6 {(i,j) in E, (top,s,t) in Eltot}:
	qa[i,j,top,s,t] <= 2 - q[i,j,top,s,t]-q[j,i,top,s,t];

	
	

# SURVIVABILITY constraints (against double link failures)

s.t. flowdoublefailures{(i,j) in E, (a,d) in E, (top,s,t) in Eltot}:
	2*(l[i,j,a,d,top,s,t]) - qa[i,j,top,s,t] - qa[a,d,top,s,t] <= 1;

s.t. flowdoublefailures2{(i,j) in E, (a,d) in E, (top,s,t) in Eltot}:
	2*l[i,j,a,d,top,s,t] - qa[i,j,top,s,t] - qa[a,d,top,s,t] >= 0;


s.t. survivability{(i,j) in E, (a,d) in E, top in TOP, k in POWERSET2[top] diff {0,2**m[top]-1}}:
	sum{(s,t) in SUBE2tot[top,k]} l[i,j,a,d,top,s,t] <= card(SUBE2tot[top,k]) - 1;
	
#s.t. capacity{(i,j) in A}:
#	sum{(top,s,t) in Btot} q[i,j,top,s,t]<= cap[i,j];	




#Virtual links down due to a double physical link failure
s.t. downVirLinks{(top,s,t) in Eltot, k in COMB, (i,j) in DF[k]}:
	vld[top,s,t,k] >= qa[i,j,top,s,t];	

s.t. downVirLinks2{(top,s,t) in Eltot, k in COMB}:
	vld[top,s,t,k] <= sum{(i,j) in DF[k]} qa[i,j,top,s,t];	


# AVAILABILITY constraints
s.t. cutsetsDown{top in TOP, h in POWERSET2[top] diff {0,2**m[top]-1}, k in COMB, (s,t) in SUBE2tot[top,h]}:
	avc[top,h,k] <= vld[top,s,t,k];
		
s.t. cutsetsDown2{top in TOP, h in POWERSET2[top] diff {0,2**m[top]-1}, k in COMB}:
	avc[top,h,k] >= (sum{(s,t) in SUBE2tot[top,h]} vld[top,s,t,k]) - (card(SUBE2tot[top,h]) -1);

s.t. virtNetDown{top in TOP, h in POWERSET2[top] diff {0,2**m[top]-1}, k in COMB}:
	av[top,k] >= avc[top,h,k];

s.t. virtNetDown2{top in TOP, k in COMB}:
	av[top,k] <= sum{h in POWERSET2[top] diff {0,2**m[top]-1}} avc[top,h,k];