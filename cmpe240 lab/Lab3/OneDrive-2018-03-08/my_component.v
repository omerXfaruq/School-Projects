module mycomponent (
    output Z,
    input [1:0]Y,
    input [2:0]X
  );

  wire d2_or_d3, d0_not, d0_or_d2, d3_not, d2_or_d3__not;

  wire [3:0]d_output;

  reg [7:0]m_input;

  decoder_2_4 decoded(d_output, Y);

  or(d2_or_d3, d_output[2], d_output[3]);

  or(d0_or_d2, d_output[0], d_output[2]);

  not(d0_not, d_output[0]);

  not(d3_not, d_output[3]);

  not(d2_or_d3__not, d2_or_d3);

  mux_8_1 muxed(Z, m_input, X);

  always @(*) begin

    m_input[0] <= d2_or_d3;

    m_input[1] <= d0_not;

    m_input[2] <= d0_or_d2;

    m_input[3] <= d3_not;

    m_input[4] <= d_output[3];

    m_input[5] <= d3_not;

    m_input[6] = 0;

    m_input[7] <= d2_or_d3__not;

  end

endmodule //
