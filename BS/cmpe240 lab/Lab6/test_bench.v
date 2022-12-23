`timescale 1ns/1ns
module testbench();

  reg [4:0] X;
  reg [4:0] Y;
  reg [1:0] S;

     wire Cout;
    wire zero;
     wire Overflow;
     wire negative;
     wire [4:0] F;

  mymodule asd(X, Y, S, zero, negative, Overflow, Cout, F);

  initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, X, Y, S, zero, negative, Overflow, Cout, F);

    S <= 2'b00;
    X <= 5'b00000;
    Y <= 5'b00000;

    #20
    repeat(4) begin
        repeat(32) begin
            repeat(32) begin

                #2;
                Y <= Y + 1;

            end
            X <= X + 1;
        end 
                S <= S + 1; 

        end
    $finish;
  end
endmodule