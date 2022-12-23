`timescale 1ns/1ns
module mymodule(X, Y, S, zero, negative, Overflow, Cout, F);

input [4:0] Y;
input [4:0] X;
input [1:0] S;

output reg Cout;
output reg zero;
output reg Overflow;
output reg negative;
output reg [4:0] F;
		
always @(X, Y, S) begin
	case(S)
    2'b00: begin
		Overflow = 0;
        Cout = X != Y;
        negative = 0;
        F = 0;
        if(F == 0) zero = 1;
        else zero = 0;

	end
	2'b01: begin
		Overflow = 0;
        negative = 0;
        {Cout, F} = X[4:2] * Y[3:1];
        if(F == 0) zero = 1;
        else zero = 0;
	end
	2'b10: begin
		{Cout, F} = X + {Y[3],Y[2],Y[1]};
        negative = F[4];
        Overflow = ~X[4] & F[4];
        if(F == 0) zero = 1;
        else zero = 0;
	end
	2'b11: begin
    
		{Cout, F} = X + Y + 5'b00001;
		
        Overflow = ~X[4] & ~Y[4] & F[4] | X[4] & Y[4] & ~F[4];

        if(F == 0) zero = 1;
        else zero = 0;

        negative = F[4];
	end
    endcase
end
endmodule