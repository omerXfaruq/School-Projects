module destiny(y, i2, i1, i0);
  input i0, i1, i2;
  output y;

  wire i0_not;
  wire i1_not;
  wire i1_and_i2;

  wire y;

  not(i0_not, i0);
  not(i1_not, i1);
  and(i1_and_i2, i1_not, i2);
  or(y, i0_not, i1_and_i2);

endmodule
