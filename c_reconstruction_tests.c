int x=1;
char *z=3;
int m[10];
int m2[20][10];
struct lol
{
    int g1;
    int g2;
    char g3;
    int g4[4];
};


void * smalloc(long bytes){
	long lala;
	return (&lala);
}

int main()
{
	unsigned int y=1;
	int *p;
    struct lol g;
    struct lol* g_ptr;
    x=2;
	y=3;
	int arr[10][10];

	arr[4][2]=2;
	arr[0][9]=arr[y][y];
	m2[0][arr[1][1]]=1;
    /*
	for (x=0;x<y;x++)
		printf("%d\n",x);

	m[3]=m[m[y]];
	z=&x;
	z[1]=3;
	y=y+1;y++;
	*/

    g.g2=1;
    g.g4[x]=2;
    g_ptr->g3=g.g1;

	p=&y;
	*p=1;	
    

	return 0;
}

