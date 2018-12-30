`timescale 1ns/1ns
module source(y,n,s,bar,rst,clk);

  output reg [1:0] y;
  output reg [2:0] n;
  output reg [2:0] s;
  input bar;
  input rst;
  input clk;

  always @(s, bar) begin

    case (s)
      3'b000:
      begin
        if(bar == 0)
          n <= 3'b001;
        else
          n <= 3'b000;

        y <= 2'b10;
      end
      3'b001:
      begin
        if(bar == 0)
          n <= 3'b110;
        else
          n <= 3'b010;

        y <= 2'b10;
      end
      3'b010:
      begin
        if(bar == 0)
          n <= 3'b101;
        else
          n <= 3'b011;

        y <= 2'b10;
      end
      3'b011:
      begin
        if(bar == 0)
          n <= 3'b001;
        else
          n <= 3'b100;

        y <= 2'b10;
      end
      3'b100:
      begin
        if(bar == 0)
          n <= 3'b001;
        else
          n <= 3'b000;

        y <= 2'b01;
      end
      3'b101:
      begin
        if(bar == 0)
          n <= 3'b110;
        else
          n <= 3'b010;

        y <= 2'b00;
      end
      3'b110:
      begin
        if(bar == 0)
          n <= 3'b001;
        else
          n <= 3'b000;

        y <= 2'b11;
      end
      3'b111:
      begin
        if(bar == 0)
          n <= 3'b000;
        else
          n <= 3'b000;

        y <= 2'b10;
      end
    endcase
  end
    // Sync reset
  always @(rst, posedge clk) begin
    if (rst)
    s <= 3'b000;
    else
    s <= n;
  end
endmodule
