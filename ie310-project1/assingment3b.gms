Sets
    i plants / 1 * 4 /
    j customers / 1 * 5 /;
    
Parameters
    a(i) Monthly production capacity(1000 bottles) /1 290,2 220,3 180,4 280/
    b(j) Monthly Demand(1000 bottles) /1 180,2 200,3 160,4 140,5 250/;
    
TABLE C(i,j) Unit Cost by Rail 
        1       2       3       4       5
    1   8.5     7       8       6.5     9
    2   7.5     8       7       10      8.5
    3   11      6       6.5     8       7
    4   9       7       12      6       7.5;
    
TABLE D(i,j) Unit Cost by Ship 
        1       2       3       4       5
    1   5.5     6       10000   3.5     4
    2   3       4.5     4       6.5     6
    3   10000   10000   3       4       4.5
    4   5       4.5     7       3       10000;
    
TABLE E(i,j) Investment Cost for Ships
        1       2       3       4       5
    1   40      60      100000  40      80
    2   60      40      80      20      40
    3   100000  100000  80      60      100
    4   100     60      60      80      100000;
    
TABLE F(i,j) Unit Cost By Ship(Merged train costs for not feasible parts)
        1       2       3       4       5
    1   5.5     6       8       3.5     4
    2   3       4.5     4       6.5     6
    3   11      6       3       4       4.5
    4   5       4.5     7       3       7.5;

TABLE G(i,j) Investment Cost for Ships (Merged train for not feasible parts)
        1       2       3       4       5
    1   40      60      0       40      80
    2   60      40      80      20      40
    3   0       0       80      60      100
    4   100     60      60      80      0;

TABLE H(i,j) Renting Cost for Ships
        1       2       3       4       5
    1   350000  350000  0       350000  350000  
    2   350000  350000  350000  350000  350000  
    3   0       0       350000  350000  350000  
    4   350000  350000  350000  350000  0;

options
optcr=0;

SCALAR
M big M /1000000000/; 

Variables
x(i,j) shipment quantities from plant i to customer j
z total transportation cost;

Positive variable x;
free variable z;

Binary variable
r(i,j) check flow from plant i to customer j
*r(i,j) is 1 if there is a flow from plant i to customer j.
        

Equations
cost    objective function
constraint1(i) constraint of production
constraint2(j) constaraint of monthly demand
constraint3(i,j) constraint of renting or not renting over shipping
constraint4 the maximum number of ships rented cannot exceed 5
constraint5     constraint of 3-3 and 1-4 route 
;

constraint1(i).. sum(j,x(i,j)) =l= a(i)*1000;
constraint2(j).. sum(i,x(i,j)) =g= b(j)*1000;
constraint3(i,j).. x(i,j) =l= r(i,j)*M;
constraint4.. sum(i,sum(j,r(i,j)))-r('1','3')-r('3','1')-r('3','2')-r('4','5') =l= 5;
constraint5.. r('3','3')+r('1','4') =l= 1;
cost.. sum(j,sum(i,(x(i,j)*F(i,j) + H(i,j)*r(i,j)))) =e= z;

model assingment3b /all/;
solve assingment3b using MIP minimizing  z;
display x.l,r.l,z.l;

    
    
    


