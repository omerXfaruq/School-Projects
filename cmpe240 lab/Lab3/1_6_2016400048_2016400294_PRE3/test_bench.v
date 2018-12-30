`timescale 1ns / 1ns
module TestBench();

reg [2:0]X; reg [1:0]Y;

wire Z;

reg [1:0]y_c; reg [2:0] x_c;

mycomponent my_decode_mux(Z, Y, X);

initial begin
	$dumpfile("TimingDiagram.vcd");
	$dumpvars(0, Z, Y, X);

  y_c = 0;


  repeat(4) begin

    Y = y_c;

    x_c = 0;

    repeat(8) begin

      X = x_c;

      x_c = x_c + 1;

      #20;
    end

    y_c = y_c + 1;
  end

	$finish;
end

endmodule
