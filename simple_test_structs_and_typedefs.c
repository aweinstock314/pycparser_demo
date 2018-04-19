int x;
int y[100];


typedef struct boom
{
    int b;
    int x;
} bam;

typedef bam bom;
bom grenade;

struct lol
{
    int a;
    int b;
    int* m;
    char c[10];
	char* e[5];
	char d[];
} *haha;

struct lol hehe;




int a_fun(int x,int* y)
{
    int b=1;
    int *c;
    struct lol m;
    struct lol * n;

	b=4;

    return 0;
}


struct ll
{
    int a;
};

int z[10];

struct lol * muahaha;

int main()
{
	char d[x];
	char j[50];
	char *k;
	unsigned int n;

	n=(unsigned int) 2;
	d[1]='1';
	d[n]=n;
	d[d[n]]=n;
	j[j[2]]='4';
	k=&j;
	k=&j[0];
	k[3]='2';	
	a_fun(3,4);
	hehe.a=4;
	(&hehe)->b=3;
	*(k+2)='1';
	*(hehe.e[2])='2';

	return 0;
}

