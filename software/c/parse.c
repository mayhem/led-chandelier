#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_CODE_LEN      512
#define VALUE_SIZE          2
#define ARG_VALUE           0
#define ARG_FUNC            1
#define ARG_COLOR           2
#define ARG_BOTTLE_SUPPLIED 3

uint8_t parse_func(char *code, int len, int index)
{
    uint8_t id, num_args, i, arg;
    uint16_t args, arg_index, value;

    id = code[index] >> 4;
    num_args = code[index] & 0xF;

    printf("id %d args %d\n", id, num_args);

    args = (code[index + 2] << 8) | code[index + 1];
    arg_index = index + 3;
    for(i = 0; i < num_args; i++)
    {
        arg = (args >> (i * 2)) & 0x3;
        if (arg == ARG_VALUE)
        {
            value = *((uint16_t *)&code[arg_index]); 
            arg_index += VALUE_SIZE;
            printf("  value %d\n", value);
        }
        else if (arg == ARG_FUNC)
        {
            printf("  func\n");
            arg_index = parse_func(code, len, arg_index);
        }
        else if (arg == ARG_COLOR)
        {
            uint8_t col[3];

            col[0] = code[arg_index++];
            col[1] = code[arg_index++];
            col[2] = code[arg_index++];
            printf("  color %d, %d, %d\n", col[0], col[1], col[2]);
        }
        else
            printf("  unknown ");
    }
    if (arg_index < len)
        arg_index = parse_func(code, len, arg_index);

    return arg_index;
}

int main(int argc, char *argv[])
{
    FILE *fp;
    int rd, index = 0;
    char code[MAX_CODE_LEN], pair[3], ch;
    
    if (argc < 2)
    {
        printf("parse <bin file>\n");
        exit(-1);
    }
    fp = fopen(argv[1], "rb");
    if (!fp)
    {
        printf("Cannot open %s\n", argv[1]);
        exit(-1);
    }
    pair[2] = 0;
    for(index = 0;; index++)
    {
        rd = fread(pair, 1, 2, fp);
        if (rd < 2)
            break;
        sscanf(pair, "%02X", &ch);
        code[index] = ch;
        printf("%02X ", ch);
    }
    printf("\n");

    parse_func(code, index, 0);

    return 0;
}
