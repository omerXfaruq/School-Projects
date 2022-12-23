#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "csim.h"

/**********************************************************************
Function    : setSizesOffsetsAndMaskFields
Description : Sets the following fields in cache "acache"

  acache->numways : The number of ways
  acache->blocksize: The size of one block, in bytes
  acache->numsets: The number of sets in the cache
  acache->numBitsForBlockOffset: The number of bits of block offset
  acache->numBitsForIndex: The number of bits of Index 
  acache->VAImask: An andmask the size of the index field
  acache->VATmask: An andmask the size of the tag field
***********************************************************************/

void setSizesOffsetsAndMaskFields(cache* acache, unsigned int size, unsigned int assoc, unsigned int blocksize);

/**********************************************************************
Function    : getindex
Description : returns the set index, given an address
***********************************************************************/
unsigned long long getindex(cache* acache, unsigned long long address);

/**********************************************************************
Function    : gettag
Description : returns the tag, given an address
***********************************************************************/
unsigned long long gettag(cache* acache, unsigned long long address);

/**********************************************************************
Function    : writeback
Description : writes back the entire cache line at index waynum into the
              next level of cache (e.g. L1->L2 or L2->Mem, etc.)
***********************************************************************/
void writeback(cache* acache, unsigned int index, unsigned int waynum);

/**********************************************************************
Function    : fill
Description : fills (i.e. reads) the entire cache line that contains address
              "address" from the next level of cache/memory and places the 
              read values into the current level of cache at index, waynum
***********************************************************************/
void fill(cache* acache, unsigned int index, unsigned int waynum, unsigned long long address);
