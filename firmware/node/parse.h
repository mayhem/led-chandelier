#ifndef __PARSE_H__
#define __PARSE_H__

#include "source.h"
#include "filter.h"

extern uint32_t g_speed;
    
void heap_setup(uint8_t *heap);
void *heap_alloc(uint8_t *heap, uint8_t bytes);
void *parse(uint8_t *code, uint16_t len, uint8_t *heap);
void evaluate(s_source_t *src, uint32_t t, color_t *color);

void set_color_filter(int32_t h_shift, int32_t s_shift, int32_t v_shift);

#endif
