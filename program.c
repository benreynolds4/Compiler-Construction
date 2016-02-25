//Ben Reynolds - Task 3 13309656
#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern char* yytext;
#define END -1

int main (int argx, char** argv) {
	int wc = 0;
	int code; 
	while ((code = yylex()) != END) {
		if(code == 1) {
			printf("<ID:  %s>\n", yytext);
		}
		else if(code == 2) {
			printf("<INT:  %s>\n", yytext);
		}
		else if(code == 3) {
			printf("<STRING:  %s>\n", yytext);
		}
		else if(code == 4) {
			printf("<LPAR:  %s>\n", yytext);
		}
		else if(code == 5) {
			printf("<RPAR:  %s>\n", yytext);
		}
		else if(code == 6) {
			printf("<SEMICOLON:  %s>\n", yytext);
		}
		else if (code == 7) {
			printf("<ERROR:  %s>\n", yytext);
		}
	}
	return 0;
}