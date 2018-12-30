`timescale 1ns/1ns
module testbench();

  wire [1:0] y;
  wire [1:0] n;
  wire [1:0] s;

  reg clk;
  initial clk = 1;
  always #2 clk = ~clk;

  reg rst;
  initial rst = 1;

  reg [1:0]bar;
  initial bar = 2'b00;
	
	
	always @(posedge clk) begin
	#47
	bar[0] = ~bar[0];
	end
	
	always @(posedge clk) begin
	#55
	bar[1] = ~bar[1];
	end
	
  source fsm_tester(y, n, s, bar, rst, clk);

  initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, y, n, s, bar, rst, clk);
	#15
    rst = 0;
	#4000
    $finish;
  end
endmodule