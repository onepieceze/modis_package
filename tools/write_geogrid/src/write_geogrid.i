%module write_geogrid


%{
extern int write_geogrid(char * input, int isfile, int number, int subset); 
%}

extern int write_geogrid(char * input, int isfile, int number, int subset);
