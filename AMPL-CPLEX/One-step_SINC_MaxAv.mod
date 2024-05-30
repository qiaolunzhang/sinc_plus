
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


#CUTSET of the logical topology
set SUBE{v in V, k in S[v]} := {s in S2[v,k], t in Nl[v] diff S2[v,k]: (s,t) in El[v] or (t,s) in El[v]};
set SUBE2tot{v in V, k in S[v]} := {(s,t) in El[v]: (s,t) in SUBE[v,k] or (t,s) in SUBE[v,k]};

#Number of double link failures combinations
param comb default 0;
set F := 0..comb;
#Combinations of double link failures of physical network
set DF{k in F} within N cross N default {};

#COMBINED VIRTUAL NETWORK
#nodes of the combined virtual network
set NlC ordered:= setof{v in V, nd in Nl[v]} nd;
#virtual links 
set ElC:=setof{v in V, (s,t) in El[v]} (v,s,t);

#parameter and sets useful to find the cut-sets of the combined virtual network
param mC:= card(NlC);
set POWERSET2C := 0 .. (2**mC -1);
set S2C{k in POWERSET2C} := {i in NlC : (k div 2**(ord(i)-1)) mod 2 = 1};

#CUTSET of the logical combined topology
set SUBEC{k in POWERSET2C} := {v in V,s in S2C[k], t in NlC diff S2C[k]: (v,s,t) in ElC or (v,t,s) in ElC};
set SUBE2C{k in POWERSET2C} := {(v,s,t) in ElC: (v,s,t) in SUBEC[k] or (v,t,s) in SUBEC[k]};

#directed flow variable, used for mapping virtual links in the physical network
var q{A,Btot} binary;
#undirected flow variable
var qa{E,Eltot} binary;


#virtual link down as a conseguence of a physical link down
var g{Eltot,F} binary;

#virtual network down
var av{V,F} binary;

#directed flow variable, used for the forwarding of virtual connections
#over the combined virtual network (virtual connection = virtual link of a specific VN)
var p{Btot,Btot,F} binary;
#undirected flow variable
var pa{Eltot,Eltot,F} binary;

#f=1 if a virtual connection uses a failing link
var f{Eltot,F} binary;
#f2=1 if a virtual connection uses a virtual link and that link is a failing one 
var f2{Eltot,Eltot,F} binary;


#cut-set of the combined virtual network down
var r{POWERSET2C diff{0,2**mC-1},F} binary;

#nh=1 if a virtual connection uses at least a virtual link of another VN 
var nh{v in V,El[v],F} binary;
#nh2=1 if a virtual connection is forwarded through a virtual link of another VN
var nh2{v1 in V,El[v1],v2 in V,El[v2],F: v2<>v1} binary;

#cut-set of a virtual network down in a specific comb of double link failure
var csd{v in V,S[v] diff{0,2**m[v]-1},F} binary;
#sh=0 if the virtual network doesn't need sharing (if no cutset of that VN is down)
var sh{V,F} binary;



	# MAXIMIZE AVAILABILITY	
#maximize Availability: (num_top*(comb+1)) - (sum{k in F, v in V} av[v,k]);
maximize Availability: 100*( (num_top*(comb+1)) - (sum{k in F, v in V} av[v,k]) ) - 0.1*(sum{(i,j) in A, (v,s,t) in Btot} q[i,j,v,s,t]);


# flow constraint for mapping
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



#Virtual links affected by a double physical link failure
s.t. affectedVirLinks{(v,s,t) in Eltot, k in F, (i,j) in DF[k]}:
	g[v,s,t,k] >= qa[i,j,v,s,t];	

s.t. affectedVirLinks2{(v,s,t) in Eltot, k in F}:
	g[v,s,t,k] <= sum{(i,j) in DF[k]} qa[i,j,v,s,t];	
	
	

# flow constraint for the forwarding of virtual connections over the combined virtual network
s.t. flowvirtual {(v1,s,t) in Btot, k in F, a in Nl[v1]: a=s}:
	sum{(v2,a,d) in Btot} p[v2,a,d,v1,s,t,k] - sum{(v2,d,a) in Btot} p[v2,d,a,v1,s,t,k] = 1;

s.t. flowvirtual1 {(v1,s,t) in Btot, k in F, a in Nl[v1]: a=t}:
	sum{(v2,a,d) in Btot} p[v2,a,d,v1,s,t,k] - sum{(v2,d,a) in Btot} p[v2,d,a,v1,s,t,k] = -1;

s.t. flowvirtual2 {(v1,s,t) in Btot, k in F, a in Nl[v1]: a<>s and a<>t}:
	sum{(v2,a,d) in Btot} p[v2,a,d,v1,s,t,k] - sum{(v2,d,a) in Btot} p[v2,d,a,v1,s,t,k] = 0;


# biderectional virtual links
s.t. bidirectionalityVir {(v1,s,t) in Btot, (v2,a,d) in Btot, k in F}:
	p[v2,a,d,v1,s,t,k]-p[v2,d,a,v1,t,s,k]=0;

s.t. bidirectionalityVir2 {(v1,s,t) in Btot, (v2,a,d) in Btot, k in F}:
	p[v2,a,d,v1,s,t,k]+p[v2,d,a,v1,s,t,k]<=1;

# xor needed for setting the variable pa (unidirectional flow variable)
s.t. flowvirtual3 {(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	pa[v2,a,d,v1,s,t,k] >= p[v2,a,d,v1,s,t,k]-p[v2,d,a,v1,s,t,k];
	
s.t. flowvirtual4 {(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	pa[v2,a,d,v1,s,t,k] >= p[v2,d,a,v1,s,t,k]-p[v2,a,d,v1,s,t,k];
	
s.t. flowvirtual5 {(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	pa[v2,a,d,v1,s,t,k] <= p[v2,a,d,v1,s,t,k]+p[v2,d,a,v1,s,t,k];

s.t. flowvirtual6 {(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	pa[v2,a,d,v1,s,t,k] <= 2 - p[v2,a,d,v1,s,t,k]-p[v2,d,a,v1,s,t,k];


#Map over the same virtual link if the virtual link is not down
s.t. flowvirtualSameVL{(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F: v2==v1 and a==s and d==t}:
	pa[v2,a,d,v1,s,t,k] >= (1-g[v2,a,d,k]);



# LIMIT CAPACITY SHARING
#nh2 is the same as pa considering only different topologies (nh2=1 if connection (s,t) uses another VN)
s.t. sameVNRouting{v1 in V, (s,t) in El[v1], v2 in V, (a,d) in El[v2], k in F: v1<>v2}:
	nh2[v2,a,d,v1,s,t,k] = pa[v2,a,d,v1,s,t,k];
	
#nh=1 if connection (s,t) uses at least a virtual link (a,d) of another VN (so if nh2=1 for at least a virtual link (a,d))
s.t. sameVNRouting2{v1 in V, (s,t) in El[v1], v2 in V, (a,d) in El[v2], k in F: v1<>v2}:
	nh[v1,s,t,k] >= nh2[v2,a,d,v1,s,t,k];

s.t. sameVNRouting3{v1 in V, (s,t) in El[v1], k in F}:
	nh[v1,s,t,k] <= sum{v2 in V, (a,d) in El[v2]:v1<>v2} nh2[v2,a,d,v1,s,t,k];

#Cut-set not down if at least one of its virtual links is up
s.t. cutsetDown{v in V, h in S[v] diff {0,2**m[v]-1}, k in F, (s,t) in SUBE2tot[v,h]}:
	csd[v,h,k] <= g[v,s,t,k];
		
s.t. cutsetDown2{v in V, h in S[v] diff {0,2**m[v]-1}, k in F}:
	csd[v,h,k] >= (sum{(s,t) in SUBE2tot[v,h]} g[v,s,t,k]) - (card(SUBE2tot[v,h]) -1);

#VN need sharing if at least one of its cut-sets is down
s.t. virtNetNeedSharing{v in V, h in S[v] diff {0,2**m[v]-1}, k in F}:
	sh[v,k] >= csd[v,h,k];

s.t. virtNetNeedSharing2{v in V, k in F}:
	sh[v,k] <= sum{h in S[v] diff {0,2**m[v]-1}} csd[v,h,k];

#If no cut-set of a VN is down, the connections (s,t) of that VN can not use other VNs
s.t. limitSharing{v in V, (s,t) in El[v], k in F}:
	nh[v,s,t,k] <= sh[v,k];


	
	
#AVAILABILITY contraints	

#var f2=1 if the virtual connection (s,t) uses virtual link (a,d) and (a,d) is a failing link 
s.t. virReqUseFailVirLink{(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	f2[v2,a,d,v1,s,t,k] <= pa[v2,a,d,v1,s,t,k];

s.t. virReqUseFailVirLink1{(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	f2[v2,a,d,v1,s,t,k] <= g[v2,a,d,k];

s.t. virReqUseFailVirLink2{(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	f2[v2,a,d,v1,s,t,k] >= pa[v2,a,d,v1,s,t,k] + g[v2,a,d,k] -1;
	
#var f=1 if a virtual connection (s,t) uses a failing link
s.t. virReqUseFailVirLink3{(v2,a,d) in Eltot, (v1,s,t) in Eltot, k in F}:
	f[v1,s,t,k] >= f2[v2,a,d,v1,s,t,k];

s.t. virReqUseFailVirLink4{(v1,s,t) in Eltot, k in F}:
	f[v1,s,t,k] <= sum{(v2,a,d) in Eltot} f2[v2,a,d,v1,s,t,k];


#Virtual network down if at least one of its connections can not be satisfied (so they can be satisfied only through failing links)
s.t. virtNetDown{(v,s,t) in Eltot, k in F}:
	av[v,k] >= f[v,s,t,k];

s.t. virtNetDown2{v in V, k in F}:
	av[v,k] <= sum{(v1,s,t) in Eltot: v1==v} f[v1,s,t,k];	



#Constraints to reduce the computational time of Availability
#cut-set of the combined virtual topology down
s.t. cutsetGeneralVNDown{h in POWERSET2C diff {0,2**mC-1}, k in F, (v,s,t) in SUBE2C[h]}:
	r[h,k] <= g[v,s,t,k];
		
s.t. cutsetGeneralVNDown2{h in POWERSET2C diff {0,2**mC-1}, k in F}:
	r[h,k] >= (sum{(v,s,t) in SUBE2C[h]} g[v,s,t,k]) - (card(SUBE2C[h]) -1);
#av set to 0 if no cut-set of the combined topology is down	
s.t. reduceTimeAvailability{v in V, k in F}:
	av[v,k] <= sum{h in POWERSET2C diff {0,2**mC-1}} r[h,k];
	

