`timescale 1ns / 1ns
module TestBench();

reg x2, x1, x0;
wire y;

destiny my_module(y, x2, x1, x0);

initial begin
	$dumpfile("TimingDiagram.vcd");
	$dumpvars(0, y, x2, x1, x0);

	x2 = 0; x1 = 0; x0 = 0;
	#20
	x2 = 0; x1 = 0; x0 = 1;
	#20
	x2 = 0; x1 = 1; x0 = 0;
	#20
	x2 = 0; x1 = 1; x0 = 1;
	#20
	x2 = 1; x1 = 0; x0 = 0;
	#20
	x2 = 1; x1 = 0; x0 = 1;
	#20
	x2 = 1; x1 = 1; x0 = 0;
	#20
	x2 = 1; x1 = 1; x0 = 1;
	#20
	$finish;
end

endmodule
