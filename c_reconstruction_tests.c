int x=1;
char *z=3;
int m[10];
int main(int argc, char* argv[])
{
	unsigned int y=1;
	x=2;
	y=3;
	for (x=0;x<y;x++)
		printf("%d\n",x);

	m[3]=m[m[y]];
	z=&x;
	z[1]=3;
	y=y+1;y++;
	

	return 0;
}

