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
    1   5.5     6       100000  3.5     4
    2   3       4.5     4       6.5     6
    3   10000   10000   3       4       4.5
    4   5       4.5     7       3       10000;
    
TABLE E(i,j) Investment Cost for Ships 
        1       2       3       4       5
    1   40      60      100000  40      80
    2   60      40      80      20      40
    3   100000  100000  80      60      100
    4   100     60      60      80      100000;


Variables
        x(i,j) amount of flow from plant i to customer j
        z   objective;
        
positive variable x;
free variable z;

Equations
cost    objective function
constraint1(i) constraint of production
constraint2(j) constaraint of monthly demand
;

constraint1(i).. sum(j,x(i,j)) =l= a(i)*1000;
constraint2(j).. sum(i,x(i,j)) =g= b(j)*1000;
cost.. sum(j,sum(i,x(i,j)*C(i,j)))=e=z;

model assingment1a /all/;
solve assingment1a using lp minimizing  z;
display x.l,z.l;

    
    
    


