`timescale 1ns/1ns
module source(y,n,s,i,rst,clk);

  output reg [1:0] y;
  output reg [1:0] n;
  output reg [1:0] s;
  input wire [1:0] i;
  input wire rst;
  input wire clk;

  always @(s,i) begin
	y[0]=a'b+s[1]s[0]+s[1]b;
	y[1]=s1'a+s0'ab';
	n[0]=s0'b+s1s0+s1b;
	n[1]=y[1]
    end
    // Sync reset
  always @(posedge clk) begin
    if (rst)
    s <= 2'b00;
    else
    s <= n;
  end
endmodule
