struct node{
    double value;
    int index;
    struct node* next;
};


struct node a_node;
struct node * array_of_nodes[10];


int tests_that_use_pycparser_ast_main()
{
    struct node * head;
    struct node *tmp;
    int i,j;

    /*
    head=&a_node;

    head->value=2.0;
    head->index=3;
    head->next=0;
    
    for (i=0;i<10;i++) 
        head=head->next;
    */
    
    
    for (j=0;j<10;j++)
    {
        head=0; //NULL
        for (i=0;i<3;i++) 
        {
            tmp=smalloc(sizeof(struct_node));
            tmp->value=2.0;
            tmp->index=3;
            tmp->next=head;
            head=tmp;
        }
        array_of_nodes[j]=head;
    }
    

    return 0;
}
