`timescale 1ns / 1ns
module mymodule_gate(y, x1, x0);

input x1, x0;
output y;

and(y, x1, x0);

endmodule
