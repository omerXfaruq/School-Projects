`timescale 1ns/1ns
module testbench();

  wire [1:0] y;
  wire [2:0] n;
  wire [2:0] s;

  reg clk;
  initial clk = 1;
  always #5 clk = ~clk;

  reg rst;
  initial rst = 1;

  reg bar;
  initial bar = 1;

  source barcode_reader(y, n, s, bar, rst, clk);

  initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, y, n, s, bar, rst, clk);
    #5
    rst = 0;
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 1;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 1;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    bar = 1;
    #10
    bar = 0;
    #10
    #10
    $finish;
  end
endmodule
