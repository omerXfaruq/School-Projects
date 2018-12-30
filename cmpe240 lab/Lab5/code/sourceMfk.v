`timescale 1ns/1ns
module source(y,n,s,i,rst,clk);

  output reg [1:0] y;
  output reg [1:0] n;
  output reg [1:0] s;
  input  [1:0] i;
  input rst;
  input clk;

  always @(s,i) begin
    y[0] <= (~i[1] & i[0]) | (s[1] & s[0]) | (s[1] & i[0]);
    y[1] <= (~s[1] & i[1]) | (~s[0] & i[1] & ~i[0]);
    n[0] <= (~s[0] & i[0]) | (s[1] & s[0]) | (s[1] &i[0]);
    n[1] <= (~s[1] & i[1]) | (~s[0] & i[1] & ~i[0]);
  end
    // Sync reset
  always @(posedge clk) begin
    if (rst)
      s <= 2'b00;
    else
      s <= n;
  end
endmodule
