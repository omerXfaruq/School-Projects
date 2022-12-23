#include "YOURCODEHERE.h"


/*
How to verify:

There are several ways we can verify that the cache simulation is working correctly.
1. Verify the matrix output.
2. Compare the output with the given output.
3. Check values in memory of addresses that are used. If the value is incorrect/missing from one level, go to upper level and check there as well, since we use writeback.
*/


/**********************************************************************
    Function    : lg2pow2
    Description : this help funciton for you to calculate the bit number
                  this function is not allowed to modify
    Input       : pow2 - for example, pow2 is 16
    Output      : retval - in this example, retval is 4
***********************************************************************/
unsigned int lg2pow2(uint64_t pow2) {
  unsigned int retval = 0;
  while (pow2 != 1 && retval < 64) {
    pow2 = pow2 >> 1;
    ++retval;
  }
  return retval;
}

void setSizesOffsetsAndMaskFields(cache * acache, unsigned int size, unsigned int assoc, unsigned int blocksize) {

  unsigned int localVAbits = 8 * sizeof(uint64_t * );
  if (localVAbits != 64) {
    fprintf(stderr, "Running non-portable code on unsupported platform, terminating. Please use designated machines.\n");
    exit(-1);
  }
  acache -> numways = assoc;
  acache -> blocksize = blocksize;
  int numsets = size / blocksize / assoc;
  acache -> numsets = numsets;
  int block_bit_count = lg2pow2(blocksize);
  acache -> numBitsForBlockOffset = block_bit_count;
  int index_bit_count = lg2pow2(numsets);
  acache -> numBitsForIndex = index_bit_count;
  unsigned long long b = 1;
  acache -> VAImask = ((b << (index_bit_count + block_bit_count)) - 1) & (~((b << block_bit_count) - 1));
  acache -> VATmask = ~((b << (index_bit_count + block_bit_count)) - 1);

}

unsigned long long getindex(cache * acache, unsigned long long address) {
  return (acache -> VAImask & address) >> acache -> numBitsForBlockOffset;
}

unsigned long long gettag(cache * acache, unsigned long long address) {
  return (acache -> VATmask & address) >> (acache -> numBitsForBlockOffset + acache -> numBitsForIndex);
}

void writeback(cache * acache, unsigned int index, unsigned int oldestway) {
  cacheblock evicting = acache -> sets[index].blocks[oldestway];
  unsigned long long physical_address = (
    ((unsigned long long) evicting.tag << (acache -> numBitsForIndex + acache -> numBitsForBlockOffset)) +
    ((unsigned long long) index << (acache -> numBitsForBlockOffset))
  );

  int word_count = acache -> blocksize / 8;
  for (int i = 0; i < word_count; i++) {
    StoreWord(acache -> nextcache, physical_address, evicting.datawords[i]);
    //printf("Writeback, Wrote %llu to address %llu\n",evicting.datawords[i], physical_address);
    //printf("Tag was: %u Index was: %u\n",evicting.tag, index);
    physical_address += 8;
  }
}

void fill(cache * acache, unsigned int index, unsigned int oldestway, unsigned long long address) {
  cacheblock filling = acache -> sets[index].blocks[oldestway];
  unsigned long long b = 1;
  address = address & ~((b << acache -> numBitsForBlockOffset) - 1);
  int word_count = acache -> blocksize / 8;
  for (int i = 0; i < word_count; i++) {
    filling.datawords[i] = LoadWord(acache -> nextcache, address);
    address += 8;
  }
}