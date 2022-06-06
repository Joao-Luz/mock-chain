#pragma once

#include <stdio.h>

#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
#define BYTE_TO_BINARY(byte)  \
  (byte & 0x80 ? '1' : '0'), \
  (byte & 0x40 ? '1' : '0'), \
  (byte & 0x20 ? '1' : '0'), \
  (byte & 0x10 ? '1' : '0'), \
  (byte & 0x08 ? '1' : '0'), \
  (byte & 0x04 ? '1' : '0'), \
  (byte & 0x02 ? '1' : '0'), \
  (byte & 0x01 ? '1' : '0') 

void print_binary(unsigned char* bytes, int n_bytes) {

    for (int i = 0; i < n_bytes; i++) {
        printf(BYTE_TO_BINARY_PATTERN, BYTE_TO_BINARY(bytes[i]));
    }
    printf("\n");
}

void create_mask(unsigned char* bytes, int size) {
    for (int i = 0; i < size/8; i++) {
        bytes[i] |= 0b11111111;
    }

    int rest = size % 8;

    for (int i = 0; i < rest; i++) {
        bytes[size/8] |= 0b10000000;
        if (i < rest-1) bytes[size/8] >>= 1;
    }
}

int and_mask(unsigned char* bytes, unsigned char* mask, int size) {
    int result = 1;

    for (int i = 0; i < size; i++) {
        result *= !(bytes[i] & mask[i]);
    }

    return result;
}